"""
Context-aware code snippet generators for different file types
"""
import numpy as np
from typing import List


class CodeSnippetGenerator:
    """Generate realistic code snippets based on file type"""

    PYTHON_SNIPPETS = [
        # Complete function implementations
        "def validate_email(email: str) -> bool:\n    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$'\n    return re.match(pattern, email) is not None",
        "def calculate_statistics(data: List[float]) -> Dict[str, float]:\n    return {\n        'mean': np.mean(data),\n        'median': np.median(data),\n        'std': np.std(data),\n        'min': np.min(data),\n        'max': np.max(data)\n    }",
        "async def fetch_user_data(user_id: int) -> Optional[Dict]:\n    async with aiohttp.ClientSession() as session:\n        async with session.get(f'{API_BASE_URL}/users/{user_id}') as response:\n            if response.status == 200:\n                return await response.json()\n            return None",
        "def process_dataframe(df: pd.DataFrame) -> pd.DataFrame:\n    df['timestamp'] = pd.to_datetime(df['timestamp'])\n    df = df.dropna(subset=['user_id', 'event_type'])\n    df['event_date'] = df['timestamp'].dt.date\n    return df.sort_values('timestamp')",
        "class DataPipeline:\n    def __init__(self, config: Dict[str, Any]):\n        self.config = config\n        self.logger = logging.getLogger(__name__)\n        self.processed_count = 0\n        self.error_count = 0",
        "    def transform_data(self, raw_data: List[Dict]) -> pd.DataFrame:\n        self.logger.info(f'Transforming {len(raw_data)} records')\n        df = pd.DataFrame(raw_data)\n        df = self._clean_nulls(df)\n        df = self._apply_business_rules(df)\n        self.processed_count += len(df)\n        return df",
        "    def _apply_business_rules(self, df: pd.DataFrame) -> pd.DataFrame:\n        df['status'] = df['status'].str.lower()\n        df['amount'] = df['amount'].astype(float).round(2)\n        df = df[df['amount'] > 0]\n        return df",
        "def retry_with_backoff(func, max_retries=3, initial_delay=1):\n    for attempt in range(max_retries):\n        try:\n            return func()\n        except Exception as e:\n            if attempt == max_retries - 1:\n                raise\n            delay = initial_delay * (2 ** attempt)\n            time.sleep(delay)",
        "@dataclass\nclass UserProfile:\n    user_id: int\n    email: str\n    created_at: datetime\n    preferences: Dict[str, Any]\n    \n    def to_dict(self) -> Dict:\n        return asdict(self)",
        "def parse_config_file(file_path: str) -> Dict[str, Any]:\n    with open(file_path, 'r') as f:\n        config = yaml.safe_load(f)\n    \n    required_keys = ['database', 'api_endpoint', 'timeout']\n    for key in required_keys:\n        if key not in config:\n            raise ValueError(f'Missing required config key: {key}')\n    \n    return config",
        "class CacheManager:\n    def __init__(self, ttl: int = 3600):\n        self._cache: Dict[str, Tuple[Any, float]] = {}\n        self._ttl = ttl\n    \n    def get(self, key: str) -> Optional[Any]:\n        if key in self._cache:\n            value, timestamp = self._cache[key]\n            if time.time() - timestamp < self._ttl:\n                return value\n            del self._cache[key]\n        return None",
        "def aggregate_metrics(events: List[Dict]) -> Dict[str, int]:\n    metrics = defaultdict(int)\n    for event in events:\n        event_type = event.get('type', 'unknown')\n        metrics[event_type] += 1\n        metrics['total'] += 1\n    return dict(metrics)",
        "async def batch_process_items(items: List[Any], batch_size: int = 100):\n    results = []\n    for i in range(0, len(items), batch_size):\n        batch = items[i:i + batch_size]\n        batch_results = await asyncio.gather(\n            *[process_item(item) for item in batch],\n            return_exceptions=True\n        )\n        results.extend(batch_results)\n    return results",
        "def filter_and_transform(data: List[Dict], filters: Dict) -> List[Dict]:\n    filtered = [\n        item for item in data\n        if all(item.get(k) == v for k, v in filters.items())\n    ]\n    return [\n        {k: v for k, v in item.items() if v is not None}\n        for item in filtered\n    ]",
        "class DatabaseConnection:\n    def __init__(self, connection_string: str):\n        self.connection_string = connection_string\n        self.conn = None\n    \n    def __enter__(self):\n        self.conn = psycopg2.connect(self.connection_string)\n        return self.conn\n    \n    def __exit__(self, exc_type, exc_val, exc_tb):\n        if self.conn:\n            self.conn.close()",
    ]

    TERRAFORM_SNIPPETS = [
        # Complete Azure resource definitions
        'resource "azurerm_linux_virtual_machine" "web_server" {\n  name                = "web-server-${var.environment}"\n  resource_group_name = azurerm_resource_group.main.name\n  location            = azurerm_resource_group.main.location\n  size                = "Standard_D2s_v3"\n  admin_username      = "azureuser"\n  \n  network_interface_ids = [\n    azurerm_network_interface.main.id,\n  ]\n  \n  admin_ssh_key {\n    username   = "azureuser"\n    public_key = file("~/.ssh/id_rsa.pub")\n  }\n  \n  os_disk {\n    caching              = "ReadWrite"\n    storage_account_type = "Premium_LRS"\n  }\n  \n  source_image_reference {\n    publisher = "Canonical"\n    offer     = "0001-com-ubuntu-server-focal"\n    sku       = "20_04-lts-gen2"\n    version   = "latest"\n  }\n  \n  tags = local.common_tags\n}',
        'resource "azurerm_storage_account" "data_lake" {\n  name                     = "datalake${random_string.suffix.result}"\n  resource_group_name      = azurerm_resource_group.main.name\n  location                 = azurerm_resource_group.main.location\n  account_tier             = "Standard"\n  account_replication_type = "GRS"\n  account_kind             = "StorageV2"\n  is_hns_enabled           = true\n  \n  network_rules {\n    default_action             = "Deny"\n    ip_rules                   = var.allowed_ips\n    virtual_network_subnet_ids = [azurerm_subnet.private.id]\n  }\n  \n  blob_properties {\n    versioning_enabled = true\n    change_feed_enabled = true\n  }\n  \n  tags = local.common_tags\n}',
        'resource "azurerm_kubernetes_cluster" "main" {\n  name                = "aks-${var.environment}"\n  location            = azurerm_resource_group.main.location\n  resource_group_name = azurerm_resource_group.main.name\n  dns_prefix          = "aks-${var.environment}"\n  kubernetes_version  = var.kubernetes_version\n  \n  default_node_pool {\n    name                = "default"\n    node_count          = var.node_count\n    vm_size             = "Standard_D2_v2"\n    enable_auto_scaling = true\n    min_count           = 1\n    max_count           = 5\n    os_disk_size_gb     = 30\n  }\n  \n  identity {\n    type = "SystemAssigned"\n  }\n  \n  network_profile {\n    network_plugin    = "azure"\n    load_balancer_sku = "standard"\n    network_policy    = "calico"\n  }\n  \n  tags = local.common_tags\n}',
        'resource "azurerm_postgresql_flexible_server" "main" {\n  name                   = "psql-${var.environment}"\n  resource_group_name    = azurerm_resource_group.main.name\n  location               = azurerm_resource_group.main.location\n  version                = "14"\n  administrator_login    = var.db_admin_username\n  administrator_password = var.db_admin_password\n  \n  storage_mb = 32768\n  sku_name   = "GP_Standard_D2s_v3"\n  \n  backup_retention_days        = 7\n  geo_redundant_backup_enabled = true\n  \n  high_availability {\n    mode                      = "ZoneRedundant"\n    standby_availability_zone = "2"\n  }\n  \n  tags = local.common_tags\n}',
        'module "networking" {\n  source = "Azure/network/azurerm"\n  version = "~> 5.0"\n  \n  resource_group_name = azurerm_resource_group.main.name\n  vnet_name           = "vnet-${var.environment}"\n  address_space       = var.vnet_address_space\n  \n  subnet_prefixes = [\n    var.subnet_app,\n    var.subnet_db,\n    var.subnet_gateway\n  ]\n  \n  subnet_names = [\n    "app-subnet",\n    "db-subnet",\n    "gateway-subnet"\n  ]\n  \n  tags = local.common_tags\n}',
        'locals {\n  common_tags = {\n    Environment  = var.environment\n    ManagedBy    = "Terraform"\n    Project      = var.project_name\n    CostCenter   = var.cost_center\n    DeploymentDate = timestamp()\n  }\n  \n  resource_prefix = "${var.project_name}-${var.environment}"\n  \n  app_settings = {\n    WEBSITE_NODE_DEFAULT_VERSION = "14-lts"\n    APPINSIGHTS_INSTRUMENTATIONKEY = azurerm_application_insights.main.instrumentation_key\n    DATABASE_CONNECTION_STRING = azurerm_postgresql_flexible_server.main.connection_string\n  }\n}',
        'variable "environment" {\n  description = "Environment name (dev, staging, prod)"\n  type        = string\n  validation {\n    condition     = contains(["dev", "staging", "prod"], var.environment)\n    error_message = "Environment must be dev, staging, or prod."\n  }\n}',
        'variable "location" {\n  description = "Azure region for resources"\n  type        = string\n  default     = "eastus"\n}',
        'variable "vnet_address_space" {\n  description = "Address space for virtual network"\n  type        = list(string)\n  default     = ["10.0.0.0/16"]\n}',
        'output "aks_cluster_name" {\n  description = "Name of the AKS cluster"\n  value       = azurerm_kubernetes_cluster.main.name\n}',
        'output "storage_account_primary_access_key" {\n  description = "Primary access key for storage account"\n  value       = azurerm_storage_account.data_lake.primary_access_key\n  sensitive   = true\n}',
        'terraform {\n  required_version = ">= 1.5.0"\n  \n  required_providers {\n    azurerm = {\n      source  = "hashicorp/azurerm"\n      version = "~> 3.80"\n    }\n    random = {\n      source  = "hashicorp/random"\n      version = "~> 3.5"\n    }\n  }\n  \n  backend "azurerm" {\n    resource_group_name  = "terraform-state-rg"\n    storage_account_name = "tfstatestorage"\n    container_name       = "tfstate"\n    key                  = "prod.terraform.tfstate"\n  }\n}',
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
