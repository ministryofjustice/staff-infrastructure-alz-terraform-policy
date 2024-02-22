data "azurerm_resource_group" "rg_with_resources" {
  name = "rg-test-ac-001"
  provider = azurerm.spoke
}

# data "azurerm_resource_group" "rg_hosting_eventhub" {
#   name = "rg-testing-evhns-001"
#   provider = azurerm.spoke
# }

data "azurerm_eventhub_namespace" "eventhub_namespace" {
  name                = "evhns-testing-001"
  resource_group_name = "rg-testing-evhns-001"
  provider = azurerm.spoke
}
