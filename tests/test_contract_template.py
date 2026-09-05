import copy
import json
from pathlib import Path
import unittest

from jsonschema import Draft202012Validator, FormatChecker, ValidationError
from openapi_spec_validator import validate
from referencing import Registry
from referencing.jsonschema import DRAFT202012


ROOT = Path(__file__).resolve().parents[1]
CONTRACT_URI = "urn:docs-governance:contract-template"


class ContractTemplateTest(unittest.TestCase):
    def setUp(self):
        self.contract = json.loads((ROOT / "templates/openapi.example.json").read_text())
        registry = Registry().with_resource(
            CONTRACT_URI, DRAFT202012.create_resource(self.contract)
        )
        response = self.contract["paths"]["/api/orders/{id}"]["get"]["responses"]["200"]
        self.validator = Draft202012Validator(
            {"$ref": CONTRACT_URI + response["content"]["application/json"]["schema"]["$ref"]},
            registry=registry, format_checker=FormatChecker(),
        )
        self.response = {
            "orderId": "1234567890123456789", "userName": "示例用户", "amount": 12.5,
            "status": "paid", "createdAt": "2026-09-05T10:00:00+08:00",
            "items": [{"skuId": "1234567890123456789", "title": "示例", "price": 12.5, "quantity": 1}],
        }

    def test_template_is_valid_openapi_and_accepts_serialized_response(self):
        validate(self.contract)
        self.validator.validate(json.loads(json.dumps(self.response)))

    def test_consumer_and_provider_share_the_same_rejection_rules(self):
        invalid = []
        renamed = copy.deepcopy(self.response)
        renamed["user_name"] = renamed.pop("userName")
        invalid.append(renamed)
        for field, value in (("orderId", 1234567890123456789), ("status", "unknown"),
                             ("createdAt", "yesterday"), ("amount", 1.999)):
            candidate = copy.deepcopy(self.response)
            candidate[field] = value
            invalid.append(candidate)
        for candidate in invalid:
            with self.subTest(response=candidate):
                with self.assertRaises(ValidationError):
                    self.validator.validate(json.loads(json.dumps(candidate)))


if __name__ == "__main__":
    unittest.main()
