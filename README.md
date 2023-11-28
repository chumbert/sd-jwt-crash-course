# SD-JWT notebook

This notebook was created for an interactive presentation. As such, the information contained in the notebook might be
sparse. I tried to refer to the relevant bits of specification when possible for people using this on their own.

The notebook is meant for an audience that understands what a JWT is and have basic concepts of hashing, salting, etc.
without requiring to understand the under-the-hood details.


It goes through:

1. What does an SD-JWT look like when issuing
2. What does an SD-JWT look like when presenting
3. How does a verifier link the disclosures to the signed JWT
4. Some considerations regarding cryptographic suites
5. Some privacy considerations (mainly unlinkability)

As specified [here](https://datatracker.ietf.org/doc/html/draft-ietf-oauth-selective-disclosure-jwt-05)

# Using the notebook

1. `poetry install` (don't worry about the `sd_jwt_demo does not contain any element` thing).
2. `poetry shell`
3. `jupyter notebook sd-yacht.ipynb`
