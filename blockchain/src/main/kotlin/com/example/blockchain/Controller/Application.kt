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

import io.iohk.atala.prism.api.KeyGenerator
import io.iohk.atala.prism.api.node.NodeAuthApiImpl
import io.iohk.atala.prism.crypto.derivation.KeyDerivation
import io.iohk.atala.prism.identity.PrismDid
import io.iohk.atala.prism.identity.PrismKeyType
import io.iohk.atala.prism.protos.GrpcOptions
import org.springframework.web.bind.annotation.*
import org.springframework.web.bind.annotation.GetMapping
import org.springframework.web.bind.annotation.PostMapping
import org.springframework.web.bind.annotation.RequestMapping
import org.springframework.web.bind.annotation.RestController

data class Test(
    val val1: String,
    val val2: String
)

data class NewDIDPost(
    val passphrase: String,
    val register_did: Boolean = true,
    var seed: Any = "",
    var did_canonical: Any = "",
    var did_long_form: Any = "",
    var creation_operation_id: String = ""
)

val environment = "ppp.atalaprism.io"
val grpcOptions = GrpcOptions("https", environment, 50053)
val nodeAuthApi = NodeAuthApiImpl(grpcOptions)

@RestController
@RequestMapping("/api_v1")
class Application {
    @GetMapping("/")
    fun home(): Test {
        val r1 = Test("Hello", "World")
        return r1
    }
    @PostMapping("/DID/")
    fun new_did(@RequestBody new_did: NewDIDPost): NewDIDPost {
        println("\n\nBeginning call to new_did")
        println(new_did.passphrase)
        val seed = KeyDerivation.binarySeed(KeyDerivation.randomMnemonicCode(), new_did.passphrase)
        val masterKeyPair = KeyGenerator.deriveKeyFromFullPath(seed, 0, PrismKeyType.MASTER_KEY, 0)
        val issuingKeyPair = KeyGenerator.deriveKeyFromFullPath(seed, 0, PrismKeyType.ISSUING_KEY, 0)
        val revocationKeyPair = KeyGenerator.deriveKeyFromFullPath(seed, 0, PrismKeyType.REVOCATION_KEY, 0)
        // val unpublishedDID = PrismDid.buildLongFormFromMasterPublicKey(masterKeyPair.publicKey)
        val unpublishedDID = PrismDid.buildExperimentalLongFormFromKeys(
            masterKeyPair.publicKey,
            issuingKeyPair.publicKey,
            revocationKeyPair.publicKey
        )
        new_did.seed = seed
        new_did.did_canonical = unpublishedDID.asCanonical().did.toString()
        new_did.did_long_form = unpublishedDID.did.toString()

        println("canonical: ${new_did.did_canonical}")
        println()
        println("NewDIDPost")
        NewDIDPost::class.java.methods.forEach(::println)
        println()
        println("nodeAuthApi")
        nodeAuthApi::class.java.methods.forEach(::println)
        println("Finished introspection")

        // TO DO: Optionally register the DID on the blockchain
        // if (new_did.register_did == true) {
        //     var nodePayloadGenerator = NodePayloadGenerator(
        //         unpublishedDID,
        //         mapOf(PrismDid.DEFAULT_MASTER_KEY_ID to masterKeyPair.privateKey)
        //     )
        //     val createDidInfo = nodePayloadGenerator.createDid()
        //     val createDidOperationId = runBlocking {
        //         nodeAuthApi.createDid(
        //             createDidInfo.payload,
        //             unpublishedDID,
        //             PrismDid.DEFAULT_MASTER_KEY_ID
        //         )
        //     }
        //     new_did.creation_operation_id = createDidOperationId.hexValue()
        //     println(PrismDid.DEFAULT_MASTER_KEY_ID)
        //     println(masterKeyPair.privateKey)
        // }
        return new_did
    }

    fun check_did_status() {
        // Check the status of a DID
    }

    fun issue_credential() {
        // Create a credential
    }

    fun verify_credential() {
        // Verify a credential
    }
}
