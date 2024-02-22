# Note: @15/02/2024 first pass at creating files to run the module in:  in-progress-testing-sub
# this is still a work in progress. Need to find a way of targeting the remediation at specific Resource Group rg-test-ac-001 in dev Testing Subscription.


##################
# Definitions (no assignment yet)
##################
# create definitions by looping around all files found under the Diagnostic category folder
module "definitions" {
  source = "../../policyascode/modules/definition"
  for_each = {
    for p in fileset(path.module, "../../policies/Diagnostics/*.json") :
    trimsuffix(basename(p), ".json") => pathexpand(p)
  }
  file_path           = each.value
  management_group_id = "/providers/Microsoft.Management/managementGroups/MG-P-MoJ"
}


##################
# Initiative ( clubbing policies create above into a single initiative- still no assignment yet)
##################
module "platform_diagnostics_initiative" {
  source                  = "../../policyascode/modules/initiative"
  initiative_name         = "logto_eventhub_diagnostics_initiative"
  initiative_display_name = "[EventHub]: Diagnostics Settings Policy Initiative"
  initiative_description  = "Collection of policies that deploy resource and activity log forwarders to EventHub"
  initiative_category     = "Diagnostic"
  merge_effects           = false # will not merge "effect" parameters
  management_group_id     = "/providers/Microsoft.Management/managementGroups/MG-P-MoJ"

  # Populate member_definitions with a for loop
  member_definitions = [for mon in module.definitions : mon.definition]
}

##################
# User Assigned Managed Identity and granting it RBAC on resources and eventhub
##################

resource "azurerm_user_assigned_identity" "eventhub_uami" {
  resource_group_name = data.azurerm_resource_group.rg_with_resources.name
  location            = "uksouth"
  name                = "eventhub-uami"
  provider = azurerm.spoke
}

# Role assignment for the first resource group
resource "azurerm_role_assignment" "rg_with_resources_contributor" {
  scope                = data.azurerm_resource_group.rg_with_resources.id
  role_definition_name = "Contributor"
  principal_id         = azurerm_user_assigned_identity.eventhub_uami.principal_id

}

# Role assignment on the eventhub namespace
resource "azurerm_role_assignment" "eventhub_dataowner" {
  scope                = data.azurerm_eventhub_namespace.eventhub_namespace.id
  role_definition_name = "Azure Event Hubs Data Owner"
  principal_id         = azurerm_user_assigned_identity.eventhub_uami.principal_id
}


##################
# Initiative Assignment( Finally assigning the initiative at rg level)
##################

module "set_rg_configure_diag_initiative" {
  source                 = "../../policyascode/modules/set_assignment"
  initiative             = module.platform_diagnostics_initiative.initiative
  assignment_scope       = "/subscriptions/4b068872-d9f3-41bc-9c34-ffac17cf96d6/resourceGroups/rg-test-ac-001"
  assignment_description = "Ensure Azure Platform resource log data is streamed to Event Hub"
  assignment_enforcement_mode = true
  assignment_location    = "uksouth"
  
  # resource remediation options
  re_evaluate_compliance = true                                                                                #var.re_evaluate_compliance
  skip_remediation       = false                                                                              #var.skip_remediation
  skip_role_assignment   = false                                                                               #var.skip_role_assignment
  role_assignment_scope  = "/subscriptions/4b068872-d9f3-41bc-9c34-ffac17cf96d6/resourceGroups/rg-test-ac-001" #data.azurerm_management_group.team_a.id # set explicit scopes (defaults to assignment scope)

  assignment_parameters = {
    eventHubName                = "evh-testing-resource-logs"
    eventHubAuthorizationRuleId = "/subscriptions/4b068872-d9f3-41bc-9c34-ffac17cf96d6/resourcegroups/rg-testing-evhns-001/providers/Microsoft.EventHub/namespaces/evhns-testing-001/authorizationrules/RootManageSharedAccessKey"
    resourceLocation            = "uksouth"
  }

  # User Assigned Managed Identity

  identity_ids = [azurerm_user_assigned_identity.eventhub_uami.id]


}