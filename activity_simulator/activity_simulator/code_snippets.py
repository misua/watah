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
        "from typing import List, Dict",
        "def process_data(df):",
        "    return df.dropna()",
        "class DataProcessor:",
        "    def __init__(self):",
        "        self.data = []",
        "if __name__ == '__main__':",
        "    print('Running')",
        "for item in items:",
        "    result.append(item)",
        "try:",
        "    data = load_data()",
        "except Exception as e:",
        "    logger.error(f'Error: {e}')",
        "async def fetch_data():",
        "    return await client.get()",
        "with open('file.txt') as f:",
        "    content = f.read()",
        "result = [x for x in data if x > 0]",
        "df = pd.DataFrame(data)",
        "model.fit(X_train, y_train)",
        "predictions = model.predict(X_test)",
        "plt.plot(x, y)",
        "plt.show()",
        "self.config = config",
        "return {'status': 'success'}",
        "logger.info('Processing complete')",
        "assert result == expected",
        "raise ValueError('Invalid input')",
    ]

    TERRAFORM_SNIPPETS = [
        'resource "aws_instance" "web" {',
        "  ami           = var.ami_id",
        "  instance_type = var.instance_type",
        "}",
        'variable "region" {',
        '  type    = string',
        '  default = "us-east-1"',
        'output "instance_id" {',
        "  value = aws_instance.web.id",
        'data "aws_ami" "ubuntu" {',
        "  most_recent = true",
        'provider "aws" {',
        "  region = var.region",
        'module "vpc" {',
        '  source = "./modules/vpc"',
        "  tags = {",
        '    Environment = "production"',
        "  }",
        "locals {",
        '  common_tags = {',
        '    Project = "demo"',
        "terraform {",
        '  required_version = ">= 1.0"',
        "  backend = {",
        '    bucket = "terraform-state"',
        "count = var.instance_count",
        "for_each = var.subnets",
        "depends_on = [aws_vpc.main]",
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
        pass

    def get_snippet(self, file_extension: str = None) -> str:
        """Get a random code snippet based on file extension"""
        if file_extension == ".py":
            snippets = self.PYTHON_SNIPPETS
        elif file_extension == ".tf":
            snippets = self.TERRAFORM_SNIPPETS
        else:
            snippets = self.GENERIC_CODE

        return np.random.choice(snippets)

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
