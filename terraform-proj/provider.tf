// Signle line Commnet
/* Multi line */

terraform {
    required_providers {
        hy2_aws = {
            source = "hashicopr/aws"
            version = "~> 3.0"
        }
    }
}

provider "hy2_aws" {
    alias = "test"
}