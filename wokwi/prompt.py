from untils import embed_description,platform_description, get_hardwares, remove_annotation,platform_parts,hardware_id,platform_message
def gen_template(diagram):
    def gen_inputs(diagram):
        hardwares = get_hardwares(diagram)
        hardware_type = set()
        for hardware in hardwares:
            hardware_type.add(hardware_id[hardware['type']])
        inputs = f"""### Components Infomration"""
        cur_descriptions = [embed_description[i]['description'] for i in hardware_type]
        inputs += "\n" + "---\n".join(cur_descriptions)
        inputs += f"""
### Components Usage
{hardwares}
### Connections
{diagram['connections']}
### Tasks
Given the hardware and the connections, your task is to write a problem description and a solution for the problem. Follow is the detailed rules for the problem description and the solution.

**problem description** :
1. The problem should include two parts:
(1). **Task**: Explain the hardware provided for the problem and briefly describe the problem to be solved.
(2). **Detail Rules**: Describe the detailed rules of the problem. Include the state that the hardware needs to exhibit after each step of operation
2. When describing the hardware that needs to be used, you need to add () after each hardware, which contains the corresponding id for that hardware
3. You must not mention any information related to hardware wiring, as that is something the person answering this question needs to figure out.
4. All the hardwares should be used in the problem description.
5. If the state of the hardware changes over time, it is necessary to ensure that each state can be maintained for more than 2 seconds to facilitate verification.
6. Your output should be in [Description] and [/Description].

**solution** :
1. Your code should include void setup() and void loop() functions.
2. Your code should in [Arduino Code] and [/Arduino Code]
"""
        return inputs
    def get_outputs(description,solution):
        return f"""[Description]
{description}
[/Description]
[Arduino Code]
{solution}
[/Arduino Code]"""
    prompt = gen_inputs(diagram)
    return prompt


def problem_description(problem_ch, solution, diagram):
    hardwares = get_hardwares(diagram)
    return f"""# Task
Given a simple Chinese problem description, a reference arduino-uno code and the id of the hardware used, your task is to expand this Chinese problem description into a clear and rigorous **English** problem description.

This question should include two parts:
1. **Task**: Explain the hardware provided for the problem and briefly describe the problem to be solved.
2. **Detail Rules**: Describe the detailed rules of the problem. Include the state that the hardware needs to exhibit after each step of operation

# Example
Here is a example of the **English** problem description:
[English Description]
**Task**:
You are tasked with programming an Arduino to control an RGB LED (rgb1) using a button (k1).

**Detail Rules**:
Initialization: Upon powering on or resetting, the RGB LED should be off.
Button Interaction: Each press of the button K1 should cycle the RGB LED through a sequence of colors:
First Press: LED displays red.
Second Press: LED displays green.
Third Press: LED displays blue.
Fourth Press: LED turns off.
This sequence should repeat with each subsequent press of the button.
[/English Description]

# Note
1. In the **Task**, When describing the hardware that needs to be used, you need to add () after each hardware, which contains the corresponding id for that hardware
2. You must not mention any information related to hardware wiring, as that is something the person answering this question needs to figure out.
3. Your output should be in [English Description] and [/English Description].

[Chinese Description]
{problem_ch}
[/Chinese Description]
[Arduino Code]
{solution}
[/Arduino Code]
[Hardware ID]
{hardwares}
[/Hardware ID]"""

def generate_prompt(problem, diagram, hardware_lst, task, platform):
    if type(diagram) == str:
        diagram = eval(diagram)
    connections = diagram['connections']
    connections_str = ""
    for connection in connections:
        connections_str += f"{connection[:2:]}\n"
    example_connections = """["uno:GND.1", "led1:COM"]
["uno:A2", "sr1:SHCP"]
["sr1:MR", "sevseg1:COM.1"]
["rgb1:G", "uno:10"]
...
["r1:1", "bargraph1:C1"]
"""
    hardware_id = get_hardwares(diagram)
    prompt = ""
    prompt += f"""### Problem Description
{problem}
### Components Usage
{hardware_id}
Note:
**id**: the id of the component, which also mentioned in Problem Description
**type**: the type of the component, which also mentioned in Components Infomration
### Components Infomration
{platform_description[platform]}
"""
    for index, num in enumerate(hardware_lst):
        if num != 0:
            prompt += f"""---
{embed_description[index]['description']}
"""
    if task == "with_connection":
        # add connections
        prompt += f"""### Connections
{connections_str}
Note:
Each line in the list represents a single connection between two components, where the elements are formatted as "id:pin ". For example, ["uno:GND.1", "led1:COM"] indicates a connection between the GND.1 pin of the "uno" component and the COM pin of the "led1" component.
"""
        # add task
        prompt += f"""### Task
Your task is to write an Arduino code to solve the problem described above. The code should be able to work with the hardware components listed in the "Components Usage" section, and the connections listed in the "Connections" section.
Note:
1. Your code should include void setup() and void loop() functions.
2. Your code should in code block : ```arduino ```
3. The package you can use is "Servo.h"
"""
    elif task == "without_connection":
        prompt += f"""### Example Connections
Here is an example of connection format:
[CONNECTIONS]
{example_connections}
[/CONNECTIONS]
Note:
Each line in the list represents a single connection between two components, where the elements are formatted as "id:pin ". For example, ["uno:GND.1", "led1:COM"] indicates a connection between the GND.1 pin of the "uno" component and the COM pin of the "led1" component.
**id**: the id can be found in the "Problem Description" and "Components Usage" section.
**pin**: the pins can be found in the "Components Infomration" section.
"""
        prompt += f"""### Task
1. Give connections in the format like "Example Connections" section. The connections should be able to work with the hardware components listed in the "Components Usage" section.
2. write an Arduino code to solve the problem described above. The code should be able to work with the hardware components listed in the "Components Usage" section and the connections you provided.
Note:
1. Your code should include void setup() and void loop() functions.
2. Your connections should in [CONNECTIONS] and [/CONNECTIONS]
3. Your code should in [Arduino Code] and [/Arduino Code]
4. The package you can use is "Servo.h"
"""
    else:
        raise ValueError("task must be 'with_connection', 'without_connection'")
    return prompt

def translate_prompt(solution,diagram,hardware_lst,platform,target_info):
    if type(diagram) == str:
        diagram = eval(diagram)
    connections = diagram['connections']
    connections_str = ""
    for connection in connections:
        connections_str += f"{connection[:2:]}\n"
    hardware_id = []
    for hardware in diagram['parts']:
        hardware_id.append({"type": hardware['type'].replace("wokwi-", ""), "id": hardware['id']})
    prompt = f"""### Arduino Code
[Arduino Code]
{remove_annotation(solution, "cpp")}
[/Arduino Code]
### Components Usage
{hardware_id}
Note:
**id**: the id of the component, which also mentioned in Connections
**type**: the type of the component, which also mentioned in Components Infomration
### Components Information
{platform_description[platform]}
"""
    for index, num in enumerate(hardware_lst):
        if num != 0:
            prompt += f"""---
{embed_description[index]['description']}
"""
    prompt += f"""### Connections
[CONNECTIONS]
{connections_str}
[/CONNECTIONS]
Note:
Each line in the list represents a single connection between two components, where the elements are formatted as "id:pin ". For example, ["uno:GND.1", "led1:COM"] indicates a connection between the GND.1 pin of the "uno" component and the COM pin of the "led1" component.
"""
    prompt += f"""### Task
Please migrate the connections and code to another development platform while keeping the implemented functions unchanged. All hardware remains the same except for the development board. The target platform is {target_info['platform']} and the target language is {target_info['language']}. The version of the target language is {platform_message[target_info['platform']]['version']}.
{target_info['platform']} Infomration:
**id**: {platform_parts[target_info['platform']]['id']}
{platform_description[target_info['platform']]}
Note:
1. The code should be able to work with the hardware components listed in the "Components Usage" section and the connections you provided.
2. The issue of different power supply voltages is ignored: assuming that all devices can adapt to any voltage.
3. Your connections should in [CONNECTIONS] and [/CONNECTIONS]
4. Your code should in [{target_info['platform']} Code] and [/{target_info['platform']} Code]
6. First give the connection and then give the code.
"""
    return prompt