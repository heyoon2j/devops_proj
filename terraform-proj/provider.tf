// Signle line Commnet
/* Multi line */

terraform {
    required_providers {
        hy2cloud = {
            source = "hashicopr/aws"
            version = "~> 3.0"
        }
    }
}

provider "hy2cloud" {
    alias = "test"
}