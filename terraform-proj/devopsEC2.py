#!/usr/bin/env python
from constructs import Construct
from imports.aws import (
    KeyPair,
    Instance,
    InstanceNetworkInterface,
    InstanceMetadataOptions,
    InstanceRootBlockDevice,
)
from cdktf import App, TerraformStack, TerraformOutput, TerraformVariable


class DevopsEC2(TerraformStack):
    def __init__(self, scope: Construct, ns: str):
        super().__init__(scope, ns)

        devopsKeyPair = KeyPair(
            self,
            "DevopsKeyPair",
            public_key="",
            key_name="",
        )

        devopsEC2 = Instance(
            self,
            "DevopsEC2",
            count=1,
            ami="ami-0f2c95e9fe3f8f80e",
            instance_type="t2.micro",
            # Instance Configuration
            ## if want spot instance, use "spot_instance_request" resource
            subnet_id="${variable.pub_subnet_id[0]}",
            ## Public IP associate
            associate_public_ip_address=False,
            ## IAM name
            ############################## iam_instance_profile="",
            ## Shutdown case : stop or terminate
            instance_initiated_shutdown_behavior="terminate",
            ## 종료우발 방지
            disable_api_termination=True,
            ## Monitoring using CloudWatch
            monitoring=False,
            ## Tenancy:
            ### tenancy = ,
            ## Detail Option
            metadata_options=[
                InstanceMetadataOptions(
                    http_endpoint="enabled",
                    http_put_response_hop_limit=1,
                    http_tokens="optional",
                )
            ],
            ## User Data
            # user_data = "",
            # Add Storage
            root_block_device=[
                ## Root Device
                InstanceRootBlockDevice(
                    volume_type="gp2",
                    # size: GiB
                    volume_size=8,
                    # Only valid for volume_type is io1, io2, gp3
                    ## iops = ,
                    # Only valid for volume_type is gp3
                    ## throughput = ,
                    delete_on_termination=True,
                    # KMS 암호화
                    ## encrypted = ,
                    ## kms_key_id = ,
                )
            ],
            ## ebs_block_device = [],
            ## ebs_optimized =
            # Add Tag
            # Config Security Group
            security_groups=["${var.sg_id}"],
            #
            key_name=devopsKeyPair.key_name,
            # Tag
            tags={"Name": "devopsEC2"},
        )

        TerraformVariable(
            self,
            # default=
            "vpc_id",
            description="VPC ID",
            type="string",
        )

        TerraformVariable(self, "pub_subnet_id", type="list(string)")

        TerraformVariable(self, "sg_id", type="string")
