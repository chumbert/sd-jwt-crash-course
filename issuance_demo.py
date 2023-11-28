# These are just wrappers around the sd_jwt library because instantiating a new issuer or holder for each
# issuance and presentation is a bit irksome.

from typing import List, Dict

from sd_jwt.holder import SDJWTHolder
from sd_jwt.issuer import SDJWTIssuer
from jwcrypto.jwk import JWK


def issue_simple_sd_jwt(issuer_key: JWK, claims: Dict, holder_key=None, decoys=False):
    issuer = SDJWTIssuer(claims, issuer_key, add_decoy_claims=decoys, holder_key=holder_key)

    return issuer.sd_jwt, issuer.serialized_sd_jwt, issuer.ii_disclosures, issuer.sd_jwt_issuance


def create_presentation(full_issuance_payload: str, disclosed_attributes: List[str], nonce=None, aud=None, holder_key=None):
    holder = SDJWTHolder(full_issuance_payload)
    holder.create_presentation(
        {attribute: attribute for attribute in disclosed_attributes},
        nonce=nonce,
        aud=aud,
        holder_key=holder_key
    )

    return holder.sd_jwt_presentation, holder.hs_disclosures
