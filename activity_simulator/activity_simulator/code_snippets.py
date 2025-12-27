"""
Context-aware code snippet generators for different file types
"""
import numpy as np
from typing import List


class CodeSnippetGenerator:
    """Generate realistic code snippets based on file type"""

    PYTHON_SNIPPETS = [
        "import numpy as np",
        "import pandas as pd",
        "from typing import List, Dict, Optional",
        "def process_data(df):",
        "    return df.dropna()",
        "class DataProcessor:",
        "    def __init__(self, config):",
        "        self.config = config",
        "        self.data = []",
        "if __name__ == '__main__':",
        "    main()",
        "for item in items:",
        "    result.append(item)",
        "try:",
        "    data = load_data()",
        "except Exception as e:",
        "    logger.error('Error: %s', e)",
        "async def fetch_data():",
        "    return await client.get(url)",
        "with open('file.txt', 'r') as f:",
        "    content = f.read()",
        "result = [x for x in data if x > 0]",
        "df = pd.DataFrame(data)",
        "model.fit(X_train, y_train)",
        "predictions = model.predict(X_test)",
        "self.logger = logging.getLogger(__name__)",
        "return {'status': 'success', 'count': len(data)}",
        "logger.info('Processing complete')",
        "assert result == expected",
        "response = requests.get(url, timeout=30)",
        "config = yaml.safe_load(f)",
        "parser.add_argument('--input', type=str)",
        "app = Flask(__name__)",
        "@app.route('/api/data')",
        "def get_data():",
        "    return jsonify(results)",
        "conn = sqlite3.connect('db.sqlite')",
        "cursor.execute('SELECT * FROM users')",
        "data = json.loads(response.text)",
        "time.sleep(0.1)",
    ]

    TERRAFORM_SNIPPETS = [
        'resource "azurerm_virtual_machine" "main" {',
        "  name                = var.vm_name",
        "  location            = var.location",
        "  resource_group_name = var.resource_group_name",
        "  vm_size             = var.vm_size",
        "}",
        'resource "azurerm_resource_group" "main" {',
        "  name     = var.rg_name",
        '  location = "East US"',
        "}",
        'variable "environment" {',
        '  type    = string',
        '  default = "production"',
        "}",
        'output "vm_id" {',
        "  value = azurerm_virtual_machine.main.id",
        "}",
        'provider "azurerm" {',
        '  features {}',
        "  subscription_id = var.subscription_id",
        "}",
        'resource "azurerm_storage_account" "main" {',
        "  name                     = var.storage_name",
        "  resource_group_name      = var.resource_group_name",
        "  location                 = var.location",
        '  account_tier             = "Standard"',
        '  account_replication_type = "LRS"',
        "}",
        'module "networking" {',
        '  source = "./modules/networking"',
        "  vnet_cidr = var.vnet_cidr",
        "}",
        "locals {",
        "  common_tags = {",
        "    Environment = var.environment",
        "    ManagedBy   = \"Terraform\"",
        "  }",
        "}",
        "terraform {",
        '  required_version = ">= 1.0"',
        "  required_providers {",
        "    azurerm = {",
        '      source  = "hashicorp/azurerm"',
        '      version = "~> 3.0"',
        "    }",
        "  }",
        "}",
        'resource "azurerm_virtual_network" "main" {',
        "  name                = var.vnet_name",
        "  address_space       = [var.vnet_cidr]",
        "  location            = var.location",
        "  resource_group_name = var.resource_group_name",
        "}",
        "count      = var.instance_count",
        "for_each   = var.locations",
        "depends_on = [azurerm_resource_group.main]",
        "lifecycle {",
        "  create_before_destroy = true",
        "}",
    ]

    GENERIC_CODE = [
        "# TODO: implement this",
        "// Fix this later",
        "const data = [];",
        "function process() {",
        "  return true;",
        "let result = null;",
        "var config = {};",
        "return response;",
        "console.log(data);",
        "if (condition) {",
        "} else {",
        "async function() {",
        "await fetch(url);",
        "export default App;",
    ]

    def __init__(self):
        self.recent_snippets = []
        self.max_recent = 10

    def get_snippet(self, file_extension: str = None) -> str:
        """Get a random code snippet based on file extension, avoiding recent repeats"""
        if file_extension == ".py":
            snippets = self.PYTHON_SNIPPETS
        elif file_extension == ".tf":
            snippets = self.TERRAFORM_SNIPPETS
        else:
            snippets = self.GENERIC_CODE

        available = [s for s in snippets if s not in self.recent_snippets]
        
        if not available:
            self.recent_snippets = []
            available = snippets
        
        snippet = np.random.choice(available)
        
        self.recent_snippets.append(snippet)
        if len(self.recent_snippets) > self.max_recent:
            self.recent_snippets.pop(0)
        
        return snippet

    def get_multi_line_snippet(self, file_extension: str = None, lines: int = 3) -> List[str]:
        """Get multiple related code lines"""
        if file_extension == ".py":
            patterns = [
                ["import numpy as np", "import pandas as pd", "from typing import List"],
                ["def process_data(df):", "    df = df.dropna()", "    return df"],
                ["try:", "    result = process()", "except Exception as e:", "    logger.error(e)"],
                ["class DataHandler:", "    def __init__(self):", "        self.data = []"],
                ["for item in items:", "    if item.valid:", "        results.append(item)"],
            ]
        elif file_extension == ".tf":
            patterns = [
                ['resource "aws_instance" "web" {', "  ami = var.ami_id", "  instance_type = var.type", "}"],
                ['variable "region" {', '  type = string', '  default = "us-east-1"', "}"],
                ['output "id" {', "  value = aws_instance.web.id", "}"],
                ["locals {", '  env = "prod"', "}"],
            ]
        else:
            patterns = [
                ["function process() {", "  return data;", "}"],
                ["const config = {", "  enabled: true", "};"],
                ["if (condition) {", "  doSomething();", "}"],
            ]

        pattern = np.random.choice(patterns)
        return pattern[:lines] if len(pattern) >= lines else pattern


class WindowDetector:
    """Detect active window and file extension"""

    def __init__(self):
        self.last_extension = None

    def get_active_window_title(self) -> str:
        """Get active window title using Windows API"""
        try:
            import ctypes
            from ctypes import wintypes

            user32 = ctypes.windll.user32
            hwnd = user32.GetForegroundWindow()

            length = user32.GetWindowTextLengthW(hwnd)
            buff = ctypes.create_unicode_buffer(length + 1)
            user32.GetWindowTextW(hwnd, buff, length + 1)

            return buff.value
        except Exception:
            return ""

    def detect_file_extension(self) -> str:
        """Detect file extension from window title"""
        title = self.get_active_window_title()

        if ".py" in title.lower():
            self.last_extension = ".py"
        elif ".tf" in title.lower():
            self.last_extension = ".tf"
        elif ".js" in title.lower() or ".ts" in title.lower():
            self.last_extension = ".js"
        elif "vscode" in title.lower() or "code" in title.lower():
            if self.last_extension:
                return self.last_extension
            return ".py"
        else:
            self.last_extension = None

        return self.last_extension
