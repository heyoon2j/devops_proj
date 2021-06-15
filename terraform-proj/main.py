#!/usr/bin/env python
from constructs import Construct
from cdktf import App, TerraformStack, TerraformOutput, TerraformHclModule
from imports.aws import AwsProvider
from devopsVPC import DevopsVPC
from devopsEC2 import DevopsEC2


class MyStack(TerraformStack):
    def __init__(self, scope: Construct, ns: str):
        super().__init__(scope, ns)

        # define resources here

        awsProvider = AwsProvider(self, "Aws", region="ap-northeast-2")
        vpcModule = TerraformHclModule(self, "VpcModule", source=".\\vpc")
        ec2Module = TerraformHclModule(
            self,
            "Ec2Module",
            source=".\\ec2",
            variables={
                "vpc_id": "${module.VpcModule.vpc_id}",
                "pub_subnet_id": "${module.VpcModule.pub_subnet_id}",
                "sg_id": "${module.VpcModule.sg_id}",
            },
        )


app = App()
MyStack(app, "terraform-proj")
DevopsVPC(app, "terraform-proj\\vpc")
DevopsEC2(app, "terraform-proj\\ec2")

app.synth()
