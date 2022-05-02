// Copyright (C) 2022  Learnershape and contributors

// This program is free software: you can redistribute it and/or modify
// it under the terms of the GNU Lesser General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.

// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU Lesser General Public License for more details.

// You should have received a copy of the GNU Lesser General Public License
// along with this program.  If not, see <https://www.gnu.org/licenses/>.

package com.example.blockchain.controller

import io.iohk.atala.prism.api.*
import io.iohk.atala.prism.api.models.AtalaOperationId
import io.iohk.atala.prism.api.models.AtalaOperationStatus
import io.iohk.atala.prism.api.node.*
import io.iohk.atala.prism.credentials.json.JsonBasedCredential
import io.iohk.atala.prism.crypto.MerkleInclusionProof
import io.iohk.atala.prism.crypto.Sha256Digest
import io.iohk.atala.prism.crypto.derivation.KeyDerivation
import io.iohk.atala.prism.crypto.derivation.MnemonicCode
import io.iohk.atala.prism.crypto.keys.ECKeyPair
import io.iohk.atala.prism.identity.*
import io.iohk.atala.prism.protos.*
import kotlinx.coroutines.*
import kotlinx.serialization.json.Json
import kotlinx.serialization.json.JsonObject
import kotlinx.serialization.json.JsonPrimitive
import org.springframework.web.bind.annotation.*
import org.springframework.web.bind.annotation.PostMapping
import org.springframework.web.bind.annotation.RequestMapping
import org.springframework.web.bind.annotation.RestController

data class NewDIDPost(
    var mnemonic: List<String> = listOf<String>(),
    val passphrase: String,
    val register_did: Boolean = true,
    var did_canonical: Any = "",
    var did_long_form: Any = "",
    var creation_operation_id: String = "",
    var operation_hash: String = ""
)

data class CheckDIDPost(
    val creation_operation_id: String,
    var status: String = ""
)

data class NewCredentialPost(
    val content: Map<String, String>,
    val holder_did: String,
    val issuer_mnemonic: List<String>,
    val issuer_passphrase: String,
    var creation_operation_id: String = "",
    var signed_credential_content: String = "",
    var signed_credential_canonical: String = "",
    var signed_credential_proof: Any = ""
)

data class CheckCredentialPost(
    val creation_operation_id: String,
    var status: String = ""
)

data class VerifyCredentialPost(
    val signed_credential: String = "",
    val signed_credential_proof: String = "",
    var errors: List<Any> = listOf<String>()
)

data class DIDHolder(
    val masterKeyPair: ECKeyPair,
    val issuingKeyPair: ECKeyPair,
    val revocationKeyPair: ECKeyPair,
    val did: LongFormPrismDid
)

fun generate_did(mnemonic: List<String>, passphrase: String): DIDHolder {
    val seed = KeyDerivation.binarySeed(MnemonicCode(mnemonic), passphrase)
    val masterKeyPair = KeyGenerator.deriveKeyFromFullPath(seed, 0, MasterKeyUsage, 0)
    val issuingKeyPair = KeyGenerator.deriveKeyFromFullPath(seed, 0, IssuingKeyUsage, 0)
    val revocationKeyPair = KeyGenerator.deriveKeyFromFullPath(seed, 0, RevocationKeyUsage, 0)
    val unpublishedDID = PrismDid.buildExperimentalLongFormFromKeys(
        masterKeyPair.publicKey,
        issuingKeyPair.publicKey,
        revocationKeyPair.publicKey
    )
    return DIDHolder(masterKeyPair, issuingKeyPair, revocationKeyPair, unpublishedDID)
}

val environment = "ppp.atalaprism.io"
val grpcOptions = GrpcOptions("https", environment, 50053)
val nodeAuthApi = NodeAuthApiImpl(grpcOptions)

@RestController
@RequestMapping("/api_v1")
class Application {

    @PostMapping("/DID/")
    fun new_did(@RequestBody new_did: NewDIDPost): NewDIDPost {
        if (new_did.mnemonic.size == 0) {
            new_did.mnemonic = KeyDerivation.randomMnemonicCode().words
        }
        val mnemonic = MnemonicCode(new_did.mnemonic)
        val generated_did = generate_did(mnemonic.words, new_did.passphrase)
        val unpublishedDID = generated_did.did
        new_did.did_canonical = unpublishedDID.asCanonical().did.toString()
        new_did.did_long_form = unpublishedDID.did.toString()

        if (new_did.register_did == true) {
            var nodePayloadGenerator = NodePayloadGenerator(
                unpublishedDID,
                mapOf(
                    PrismDid.DEFAULT_MASTER_KEY_ID to generated_did.masterKeyPair.privateKey,
                    PrismDid.DEFAULT_ISSUING_KEY_ID to generated_did.issuingKeyPair.privateKey,
                    PrismDid.DEFAULT_REVOCATION_KEY_ID to generated_did.revocationKeyPair.privateKey
                )
            )
            val createDidInfo = nodePayloadGenerator.createDid()
            val createDidOperationId = runBlocking {
                nodeAuthApi.createDid(
                    createDidInfo.payload,
                    unpublishedDID,
                    PrismDid.DEFAULT_MASTER_KEY_ID
                )
            }
            new_did.creation_operation_id = createDidOperationId.hexValue()
            new_did.operation_hash = createDidInfo.operationHash.hexValue
        }
        return new_did
    }

    @PostMapping("/DID_status/")
    fun check_did_status(@RequestBody check_did: CheckDIDPost): CheckDIDPost {
        // Check the status of a DID
        val operation_digest = Sha256Digest.fromHex(check_did.creation_operation_id)
        val operation_id = AtalaOperationId(operation_digest)
        val status = runBlocking {
            nodeAuthApi.getOperationStatus(operation_id)
        }
        check_did.status = AtalaOperationStatus.asString(status)
        return check_did
    }

    @PostMapping("/credential/")
    fun issue_credential(@RequestBody new_credential: NewCredentialPost): NewCredentialPost {
        // Create a credential
        val credential_content = new_credential.content.mapValues {
            JsonPrimitive(it.value)
        }
        val holder_did = PrismDid.fromString(new_credential.holder_did)
        val issuer_did = generate_did(new_credential.issuer_mnemonic, new_credential.issuer_passphrase)
        val credential_claim = CredentialClaim(
            subjectDid = holder_did,
            content = JsonObject(credential_content)
        )
        var issuerNodePayloadGenerator = NodePayloadGenerator(
            issuer_did.did,
            mapOf(
                PrismDid.DEFAULT_MASTER_KEY_ID to issuer_did.masterKeyPair.privateKey,
                PrismDid.DEFAULT_ISSUING_KEY_ID to issuer_did.issuingKeyPair.privateKey,
                PrismDid.DEFAULT_REVOCATION_KEY_ID to issuer_did.revocationKeyPair.privateKey
            )
        )
        val issueCredentialsInfo = issuerNodePayloadGenerator.issueCredentials(
            PrismDid.DEFAULT_ISSUING_KEY_ID,
            arrayOf(credential_claim)
        )
        val issueCredentialBatchOperationId = runBlocking {
            nodeAuthApi.issueCredentials(
                issueCredentialsInfo.payload,
                issuer_did.did.asCanonical(),
                PrismDid.DEFAULT_ISSUING_KEY_ID,
                issueCredentialsInfo.merkleRoot
            )
        }
        new_credential.creation_operation_id = issueCredentialBatchOperationId.hexValue()
        val holderSignedCredential = issueCredentialsInfo.credentialsAndProofs.first().signedCredential
        val holderCredentialMerkleProof = issueCredentialsInfo.credentialsAndProofs.first().inclusionProof

        // println("\n\n\nmerkle proof")
        // holderCredentialMerkleProof::class.java.methods.forEach(::println)

        new_credential.signed_credential_content = holderSignedCredential.content.fields.toString()
        new_credential.signed_credential_canonical = holderSignedCredential.canonicalForm
        new_credential.signed_credential_proof = holderCredentialMerkleProof.encode()
        // holderSignedCredential.content::class.java.methods.forEach(::println)
        return new_credential
    }

    @PostMapping("/credential_status/")
    fun check_credential_status(@RequestBody check_credential: CheckCredentialPost): CheckCredentialPost {
        // Check the status of a credential
        val operation_digest = Sha256Digest.fromHex(check_credential.creation_operation_id)
        val operation_id = AtalaOperationId(operation_digest)
        val status = runBlocking {
            nodeAuthApi.getOperationStatus(operation_id)
        }
        check_credential.status = AtalaOperationStatus.asString(status)
        return check_credential
    }

    @PostMapping("/verify_credential/")
    fun verify_credential(@RequestBody verify_cred: VerifyCredentialPost): VerifyCredentialPost {
        // Verify a credential
        val proof = Json.parseToJsonElement(verify_cred.signed_credential_proof)
        val merkle_proof = MerkleInclusionProof.decode(verify_cred.signed_credential_proof)
        val pc = JsonBasedCredential.fromString(verify_cred.signed_credential)

        val status = runBlocking {
            nodeAuthApi.verify(
                signedCredential = pc,
                merkleInclusionProof = merkle_proof
            )
        }
        verify_cred.errors = status.verificationErrors
        return verify_cred
    }
}
