import unittest
import re

class TestRigFlowPlugin(unittest.TestCase):
    def setUp(self):
        self.plugin_source = """
local RigFlow = {}
RigFlow.Version = "1.0.0"
RigFlow.Config = {
    AutoTag = true,
    ValidationLevel = "Strict"
}
function RigFlow.validateRig(model)
    if not model:IsA("Model") then return false, "Not a model" end
    local humanoid = model:FindFirstChildOfClass("Humanoid")
    if not humanoid then return false, "Missing Humanoid" end
    return true, "Valid"
end
function RigFlow.applyTags(model)
    if RigFlow.Config.AutoTag then
        model:SetAttribute("RigFlowTag", "Processed")
    end
end
"""

    def test_version_format(self):
        match = re.search(r'RigFlow\.Version\s*=\s*"([^"]+)"', self.plugin_source)
        self.assertIsNotNone(match)
        self.assertRegex(match.group(1), r'^\d+\.\d+\.\d+$')

    def test_config_keys(self):
        self.assertIn("AutoTag", self.plugin_source)
        self.assertIn("ValidationLevel", self.plugin_source)

    def test_validate_rig_function_exists(self):
        self.assertIn("function RigFlow.validateRig(model)", self.plugin_source)

    def test_apply_tags_function_exists(self):
        self.assertIn("function RigFlow.applyTags(model)", self.plugin_source)

    def test_no_hardcoded_credentials(self):
        self.assertNotIn("password", self.plugin_source.lower())
        self.assertNotIn("api_key", self.plugin_source.lower())

if __name__ == '__main__':
    unittest.main()
