#!/usr/bin/env python
from constructs import Construct
from imports.aws import (
    Vpc,
    Subnet,
    NatGateway,
    InternetGateway,
    Eip,
    SecurityGroup,
    SecurityGroupIngress,
    SecurityGroupEgress,
    NetworkAcl,
    NetworkAclEgress,
    NetworkAclIngress,
    RouteTable,
    RouteTableRoute,
    RouteTableAssociation,
)
from cdktf import App, TerraformStack, TerraformVariable, TerraformOutput


class DevopsVPC(TerraformStack):
    def __init__(self, scope: Construct, ns: str):
        super().__init__(scope, ns)
        # VPC
        self.devopsVpc = Vpc(
            self,
            "devopsVPC",
            cidr_block="10.0.0.0/16",
            # IPv6 CIDR Block 사용여부
            assign_generated_ipv6_cidr_block=False,
            # 전용 테넌시 인스턴스 사용
            instance_tenancy="default",
            enable_dns_hostnames=True,
            enable_dns_support=True,
            # enable_classiclink = False,
            # enable_classiclink_dns_support = False,
            tags={"Name": "devopsVPC"},
        )

        # Subnet
        self.devopsPri_Subnet = []
        self.devopsPri_Subnet.append(
            Subnet(
                self,
                "devopsPri_Subnet1",
                # 2a, 2b, 2c, 2d
                availability_zone="ap-northeast-2a",
                cidr_block="10.0.0.0/18",
                vpc_id=self.devopsVpc.id,
                assign_ipv6_address_on_creation=False,
                tags={"Name": "devopsPri_Subnet1"},
            )
        )
        self.devopsPri_Subnet.append(
            Subnet(
                self,
                "devopsPri_Subnet2",
                availability_zone="ap-northeast-2c",
                cidr_block="10.0.128.0/18",
                vpc_id=self.devopsVpc.id,
                assign_ipv6_address_on_creation=False,
                tags={"Name": "devopsPri_Subnet2"},
            )
        )

        self.devopsPub_Subnet = []
        self.devopsPub_Subnet.append(
            Subnet(
                self,
                "devopsPub_Subnet1",
                availability_zone="ap-northeast-2a",
                cidr_block="10.0.64.0/18",
                vpc_id=self.devopsVpc.id,
                assign_ipv6_address_on_creation=False,
                # For Public IP
                map_public_ip_on_launch=True,
                # depends_on = [devopsIG.id],
                tags={"Name": "devopsPub_subnet1"},
            )
        )
        self.devopsPub_Subnet.append(
            Subnet(
                self,
                "devopsPub_Subnet2",
                availability_zone="ap-northeast-2c",
                cidr_block="10.0.192.0/18",
                vpc_id=self.devopsVpc.id,
                assign_ipv6_address_on_creation=False,
                # For Public IP
                map_public_ip_on_launch=True,
                # depends_on = [devopsIG.id],
                tags={"Name": "devopsPub_subnet2"},
            )
        )

        self.devopsEIP = Eip(self, "devopsEIP", vpc=True, tags={"Name": "devopsEIP"})
        self.devopsNATG = NatGateway(
            self,
            "devopsNATG",
            allocation_id=self.devopsEIP.id,
            subnet_id=self.devopsPub_Subnet[0].id,
            tags={"Name": "devopsNATG"},
        )

        self.devopsIG = InternetGateway(
            self, "devopsIG", vpc_id=self.devopsVpc.id, tags={"Name": "devopsIG"}
        )

        self.devopsPriRouteTable = RouteTable(
            self,
            "devops_PriRT",
            vpc_id=self.devopsVpc.id,
            route=[
                RouteTableRoute(
                    # Destination arg
                    cidr_block="0.0.0.0/0",
                    # Target arg
                    nat_gateway_id=self.devopsNATG.id,
                    carrier_gateway_id=None,
                    destination_prefix_list_id=None,
                )
            ],
            tags={"Name": "devops_PriRT"},
        )

        devopsPriRouteTable_Association = []
        for a in range(0, 2):
            devopsPriRouteTable_Association.append(
                RouteTableAssociation(
                    self,
                    "DevopsPriRouteTableAssociation" + str(a),
                    route_table_id=self.devopsPriRouteTable.id,
                    subnet_id=self.devopsPri_Subnet[a].id,
                )
            )

        self.devopsPubRouteTable = RouteTable(
            self,
            "devops_PubRT",
            vpc_id=self.devopsVpc.id,
            route=[
                RouteTableRoute(
                    # Destination arg
                    cidr_block="0.0.0.0/0",
                    # Target arg
                    gateway_id=self.devopsIG.id,
                ),
            ],
            tags={"Name": "devops_PubRT"},
        )

        devopsPubRouteTable_Association = []
        for a in range(0, 2):
            devopsPubRouteTable_Association.append(
                RouteTableAssociation(
                    self,
                    "DevopsPubRouteTableAssociation" + str(a),
                    route_table_id=self.devopsPubRouteTable.id,
                    subnet_id=self.devopsPub_Subnet[a].id,
                )
            )

        # Security Group
        self.devopsSG = SecurityGroup(
            self,
            "devopsSG",
            name="devopsSG",
            description="Security Group for devops_proj",
            vpc_id=self.devopsVpc.id,
            ingress=[
                SecurityGroupIngress(
                    description="For HTTP",
                    from_port=80,
                    to_port=80,
                    protocol="tcp",
                    # Source, 상대방의 IP 주소
                    cidr_blocks=["0.0.0.0/0"],
                    # "ipv6_cidr_blocks" : ""
                ),
                SecurityGroupIngress(
                    description="For SSH",
                    from_port=22,
                    to_port=22,
                    protocol="tcp",
                    cidr_blocks=["0.0.0.0/0"],
                    # "ipv6_cidr_blocks" : ""
                ),
            ],
            egress=[
                # Allow All
                SecurityGroupEgress(
                    from_port=0,
                    to_port=0,
                    protocol="-1",
                    cidr_blocks=["0.0.0.0/0"],
                    ipv6_cidr_blocks=["::/0"],
                )
            ],
        )

        self.devopsACL = NetworkAcl(
            self,
            "devopsACL",
            vpc_id=self.devopsVpc.id,
            ingress=[
                NetworkAclIngress(
                    # Rule Number, Ordering
                    rule_no=100,
                    # Action: allow / deny
                    action="allow",
                    cidr_block="0.0.0.0/0",
                    from_port=80,
                    to_port=80,
                    protocol="tcp",
                )
            ],
            egress=[
                NetworkAclEgress(
                    rule_no=200,
                    action="allow",
                    cidr_block="10.0.0.0/18",
                    from_port=443,
                    to_port=443,
                    protocol="tcp",
                )
            ],
            tags={"Name": "devopsACL"},
        )

        TerraformOutput(self, "vpc_id", description="VPC ID", value=self.devopsVpc.id)

        TerraformOutput(self, "vpc_cidr", value=self.devopsVpc.cidr_block)

        pub_id = []
        for a in self.devopsPub_Subnet:
            pub_id.append(a.id)
        TerraformOutput(self, "pub_subnet_id", value=pub_id)

        TerraformOutput(self, "sg_id", value=self.devopsSG.id)
