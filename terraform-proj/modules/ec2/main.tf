# Example

resource "ec2_instance" "web" {
    # Compute
    ami = "ami-0a0de518b1fc4524c"
    instance_type = "t2.micro"
    count = 1


    # Network



    # Default = null, bool
    associate_public_ip_address = false



    # Storage
    
    ebs_block_device = 
    ebs_optimized = 

    enclave_options = 



    # Start/Terminate




    hibernation = 

    disable_api_termination = 






    # Detail


    credit_specification = 


    user_data = "
    #!/bin/bash
    yum install -y git
    "
}