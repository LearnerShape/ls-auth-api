# Copyright (C) 2022  Learnershape and contributors

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.

# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


def _create_DID_testing(new_did):
    r = new_did.copy()
    r.update(
        {
            "mnemonic": [
                "midnight",
                "supreme",
                "hand",
                "pass",
                "kangaroo",
                "cage",
                "toddler",
                "beach",
                "liberty",
                "black",
                "large",
                "assist",
            ],
            "did_canonical": "did:prism:f78422a7c4d2f23016153e2e6262f3d093476b767c1b06f62f40c7623d3f5a2f",
            "did_long_form": "did:prism:f78422a7c4d2f23016153e2e6262f3d093476b767c1b06f62f40c7623d3f5a2f:Cr8BCrwBEjsKB21hc3RlcjAQAUouCglzZWNwMjU2azESIQMTAumLMPC9fU56QO6e4DTtbPwR1DHg9mCJrq_D4-IqBBI8Cghpc3N1aW5nMBACSi4KCXNlY3AyNTZrMRIhA4YfAbmK6VLiXh5VC3SERihfgh7DbcQryKyAMJlC3PaEEj8KC3Jldm9jYXRpb24wEAVKLgoJc2VjcDI1NmsxEiEDZWzXp2d-hQ9Vd_-tkvy7uQZAEFbi3fgvR66LvDK4GIM",
            "creation_operation_id": "ff7935a5274f639b6468670a1dc21d9150cbce6b624ca267351f154204b35282",
            "operation_hash": "0051feadbacd3f09194ea3a43fc5ebc11d23f71ddd47f713bbdd31faba18d12c",
        }
    )
    r["mnemonic"] = " ".join(r["mnemonic"])
    return r


def _check_DID_status_testing(operation_id):
    payload = {"creation_operation_id": operation_id, "status": "CONFIRMED_AND_APPLIED"}
    return payload


def _create_credential_testing(new_credential):
    # TODO: Identify the key items to return when SDK is working
    r = new_credential.copy()
    r.update(
        {
            "creation_operation_id": "b284163a99905f8bb9c40bd56c7e0dd678b9689d88a1fdf5041001f5bd76b7be",
            "signed_credential_content": '{"id":"did:prism:0051feadbacd3f09194ea3a43fc5ebc11d23f71ddd47f713bbdd31faba18d12c","keyId":"issuing0","credentialSubject":{"name":"test","subject":"testing2","id":"did:prism:f78422a7c4d2f23016153e2e6262f3d093476b767c1b06f62f40c7623d3f5a2f"}}',
            "signed_credential_canonical": "eyJpZCI6ImRpZDpwcmlzbTowMDUxZmVhZGJhY2QzZjA5MTk0ZWEzYTQzZmM1ZWJjMTFkMjNmNzFkZGQ0N2Y3MTNiYmRkMzFmYWJhMThkMTJjIiwia2V5SWQiOiJpc3N1aW5nMCIsImNyZWRlbnRpYWxTdWJqZWN0Ijp7Im5hbWUiOiJ0ZXN0Iiwic3ViamVjdCI6InRlc3RpbmcyIiwiaWQiOiJkaWQ6cHJpc206Zjc4NDIyYTdjNGQyZjIzMDE2MTUzZTJlNjI2MmYzZDA5MzQ3NmI3NjdjMWIwNmY2MmY0MGM3NjIzZDNmNWEyZiJ9fQ.MEUCIFcWc6v1-2a_192lmdinURvm0IQ4ReA8Q5cZDI6gZS96AiEAwpbSkHun9Yh0PO7ZtUlhgjqR0GirmxwY4SJkROXwyYs",
            "signed_credential_proof": '{"hash":"22e7ca77fc1e526af82e9ee54ba97be5d19660718e168daccbf54f2f4ce26fda","index":0,"siblings":[]}',
            "signed_credential_hash": "d7277db099d87bf665d98e48ca34edd97a14d85ea195115dd7201e28c376fa01",
            "operation_hash": "77ceed51ae3afe60a53ce5884b9090f6e3ae551bd39ea8100b583c0e3a85f092",
            "batch_id": "00f60275644bc492c411964749cd0a5c5374e6d4b4ad32a850d4148a866a262e",
        }
    )
    return r


def _check_credential_status_testing(operation_id):
    payload = {
        "creation_operation_id": operation_id,
        "status": "CONFIRMED_AND_APPLIED",
        "transaction_id": "e735072df13669b8e41176c4ba2ac89a57a0bc179715403edd2631898fa82a38",
    }
    return payload


def _verify_credential_testing(payload):
    payload["errors"] = []
    return payload


def _revoke_credential_testing(payload):
    payload[
        "revocation_operation_id"
    ] = "bc1715a086a6dfdc0054477cc0ea8b95a81ffa9e97a10ee11c650079d31ed131"
    return payload


def _check_credential_revocation_testing(operation_id):
    payload = {
        "revocation_operation_id": operation_id,
        "status": "CONFIRMED_AND_APPLIED",
        "transaction_id": "fdc6a248be1e098cc10b00c229e51ed732ff905820f3773fcfa4e878c743ac75",
    }
    return payload
