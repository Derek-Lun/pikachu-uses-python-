Group 10: Candice Lin, David Law, Derek Lun, Kelvin Au
Slice Name: ubc_eece411_5
Date: 2015-2-9

Design choices for the monitoring service
Two message distributing algorithms were proposed during our search stage, the epidemic protocol and the hierarchical model. The hierarchical model was chosen for its simplicity and easier implementation.

System Architecture
This monitoring service uses a hierarchical model. Using the equation (# of nodes) ^(l/layer), we can determine how many nodes should be grouped under one parent. The root node will select the first node that is alive from each group as the parent node by pinging it. The parent will repeat the process until only child nodes are left. The child will collect its performance data and the data back to the parent. The parent will send the children's information along with its information to its parent. This process repeats until the information reaches the root. The root node will collect all data and displayed the information on a webpage.

Limitations
The project requires installing Node.js on all nodes. We decided to use Node.js ver.0.8.3 because of the limit of yum software version. The latest Node.js requires Python 2.6 and GCC 4.2. Yum offers up to Python 2.5.1 and GCC 4.1.2. Once Node.js is installed on all nodes involved in the monitoring service , the user can begin the monitoring service. 

Instruction

Access our monitoring server by the URL: http://ec2-54-187-198-162.us-west-2.compute.amazonaws.com/EECE411_A2_master_node/master.html

The result of nodes’ status are displayed on the webpage. The data are updated automatically every 5 minutes, or through the “Update” button. 

Node status includes:
Hostname
IP Address
Alive Status
Permission To Login
Disk Space Used
Disk Space Available
Uptime
Current Load

When the Alive Status is “NO” or Permission To Login is “No”, “N/A” will be displayed on Disk Space Used, Disk Space Available, Uptime, and Current Load.

During the update, a new node will be inserted to the bottom of the table, and a deleted node will be removed from the table, while the status of all existing nodes will be updated.


