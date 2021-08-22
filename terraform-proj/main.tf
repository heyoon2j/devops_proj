locals {
    hy2provider = {
        hy2cloud = hy2cloud.test
    } 
}

module "compute" {
    source = "./modules/ec2"

    providers = {
        hy2cloud = hy2cloud.test
    }
}

module "network" {
    source = "./modules/vpc"

    providers = {
        hy2cloud = hy2cloud.test
    }
}
