variable "environment" {
  default     = "dev"
  description = "The Environment name, i.e dev, staging, qa, preprod, test, prod..."
}

variable "tenant_id" {
  description = "Tenant id"
}

variable "subscription_id" {
  description = "Testing subscription id"
}
