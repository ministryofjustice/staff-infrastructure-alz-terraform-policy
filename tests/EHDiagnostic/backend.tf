terraform {
  backend "azurerm" {
    # Not required when run in pipeline, only required for command line testing
    storage_account_name = "samojtfstate001"
    resource_group_name  = "rg-terraform-statefiles-001"
    container_name       = "tfstate"
    key                  = "testingmod01.terraform.tfstate"
  }
}
