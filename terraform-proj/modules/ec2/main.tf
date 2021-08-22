# Example

resource "ec2_instance" "web" {
    ########## Compute ##########
    ami = "ami-0a0de518b1fc4524c"
    instance_type = "t2.micro"
    count = 1

    ## Add Network Interface
    ## Terraform으로 관리하기 위해서는 "aws_network_interface" 와 "aws_network_interface_attachment"를 사용하는 것이 좋다.
    ## network_interface = 


    ########## Purchase Option ##########
    ## Tenancy, "default"(default) / "dedicated" / "host"
    tenancy = "default"

    ## ID of a dedicated Host, Tenancy가 "" 인 경우
    ## host_id = ""


    ########## Network ##########
    ## Subnet
    subnet_id = ""

    ## Public IP Association : null(default) / true / false
    associate_public_ip_address = false

    ## Placement Group Name
    ## 사용하기 위해서는 "aws_placement_group"을 먼저 만들어야 한다.
    ## placement_group = ""

    ## Security Group List
    security_groups = [
        ""
    ]


    ########## Storage ##########
    root_block_device = {        
        volume_type = ""

        ## Volume Size (GiB), 8 ~ 
        volume_size = 8

        ## volume_type에 따라 설정할 수 있다.
        ## iops = 
        ## throughput = ""

        delete_on_termination = true
        
        ## 암호화, false(defulat) / true
        encrypted = false

        ## encrypted(true)에 따라 설정할 수 있다.
        ## kms_key_id = ""

        tags = {
        }
    }
    ## Add EBS, Use "aws_network_interface" and "aws_network_interface_attachment"
    ## Terraform으로 EBS를 관리하려면 EBS Resource를 생성하여 붙여야 된다.
    ## ebs_block_device = [{}]
    ## ebs_optimized = 


    ########### Start/Terminate ###########
    ## Shutdown behavior : "stop"(default) / "terminate"
    instance_initiated_shutdown_behavior = "terminate"

    ## 우발적인 종료로부터 보호
    ## API를 이용하여 종료가능하도록 못하게 할지 여부, true / false
    disable_api_termination = false

    ## 최대 절전 모드, true / false(default)
    hibernation = false


    ########## Detail ##########
    ## IAM Profile
    ## iam_instance_profile = ""

    ## Key Pair, ""(default)
    ## Key 없이 사용하려면 User Data에서 Password를 사용할 수 있게 작업해야 한다.
    key_name = ""

    ## CloudWatch Monitoring, true / false(default)
    monitoring = true

    ## Meta Data
    metadata_options = {
        ## Whether to use Meta Data(사용여부), "enabled"(default) / "disabled"
        http_endpoint = "enable"

        ## HTTP PUT 응답 홉 제한 수, 1(default) ~ 64
        http_put_response_hop_limit = 1

        ## Session Token 필요여부, "optional"(default) / "required"
        ## "optional" = Version 1 & Version 2 / "required" = Version 2
        http_tokens = "optional"
    }

    ## User Data
    user_data = "
    #!/bin/bash
    yum install -y git
    "

    ## User Data encoding to base64
    ## user_data_base64 = ""

    ## Tags
    tags = {
        Name = "web"
    }
}


resource "aws_lb_target_group" "web_target_grouop" {
    name = ""

    ## Name preix, 6자 초과 불가
    ## 지정된 접두사로 고유한 이름을 만든다.
    ## name_prefix = ""

    ## Algorithm Type, "round_robin"(default) / "least_outstanding_requests"
    load_balancing_algorithm_type = "round_robin"

    ## Target Type, "instance"(default) / "ip" / "lambda"
    target_type = "instance"


    ## Protocol Version, "HTTP/1.1" / "HTTP/2" / "GRPC"
    protocol_version = "HTTP/2"

    ## vpc_id, if Target Type = "ip" or "instance"
    vpc_id = ""

    ## Protocol to use for routing traffic to the targets
    ## "HTTP" / "HTTPS" / "TCP" / "TCP_UDP" / "UDP" / "TLS" / "GENEVE"/
    protocol = ""

    ## Port on which targets receive traffic
    ## Port, if Target Type = "ip" or "instance"
    port = 


    ## 기다리는 시간,사용되지 0 ~ 3600 second (default: 300)
    deregistration_delay = 


    ########## Health Check ##########
    health_check = {
        # Whether health checks are enabled, true(Defulat) / false
        enalbed = true

        path = "/"

        ## Protocol to use to connect with the target, "HTTP" (Default) / "HTTPS"
        protocol = "HTTP"

        ## Port to use to connect with the target, "traffic-port"(Default) / 1 ~ 65535
        port = "traffic-port"

        ## 정상으로 간주하기까지 필요한 연속적 상태 검사 성공 횟수
        ## 2 ~ 10 (Default 3)
        healthy_threshold = 5

        ## 비정상 상태로 간주하기까지 필요한 연속적 상태 검사 실패 횟수
        ## 2 ~ 10 (Default 3)
        unhealty_threshold = 5

        ## Health check 하는 사이 간격, 5 ~ 300s (Default 30)
        interval = 30

        ## Health check 요청에 대한 기다리는 시간, 2 ~ 120s (Default 5)
        ## 해당 시간이 지나면 실패로 간주
        timeout = 

        ## Target으로부터 응답 성공을 확인할 때 사용하는 HTTP 코드
        ## 여러 값 지정가능 (ex> 200~202 => "200,202" )
        matcher = "200,202"

    }

}


resource "aws_lb" "web_alb" {
    
    name = ""

    ## Type "application" (Default) / "gateway" / "network" 
    load_balancer_type = 

    ## If true, the LB will be internal
    ## If false, the LB will locate at Public Subnet (Interent)
    internal = false

    ## Type of IP address, "ipv4" / "dualstack" : ipv4 + ipv6
    ip_address_type = "ipv4"


    ########## Network Mapping ##########
    ## subnets = 
    subnet_mapping = {
        subnet_id = []

        ## The allocation ID of Elastic IP address
        ## allocation_id = ""

        ## Option
        ## private_ipv4_address = 
        ## ipv6_address = 
    }

    ## Custromer IPv4 Pool
    ## customer_owned_ipv4_pool = 

    ## Only valid for application
    security_groups = []

    access_logs = {
        ## true / false (Defulat)
        enabled = false

        ## S3 bucket
        ## bucket = 
        ## prefix = 
    }

    ## Connection Idle time (second), Default 60s
    idle_timeout = 60

    ## HTTP/2 사용가능 여부
    enable_http2 = true

    ## true / false (Default)
    enable_deletion_protection = false

    tags = {

    }
}


resource "aws_lb_listener" "web_alb_listener" {

    


}


