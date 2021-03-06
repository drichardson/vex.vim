import json
import subprocess

# vcc gives us 2 things: a list of VEX context names and and a way to dump the
# VEX functions and global variables from each VEX context.
# We use these 2 things to build a single uber context that is the union of all
# other contexts. This uber context is used for completion since Vim, running
# as an external editor from Houdini, has no idea which specific context it is in.
#
# vcc must be in your PATH. One way to do this is to run this python script
# from the Houdini Command Line Tools.
#
# For more information on vcc, see:
# https://www.sidefx.com/docs/houdini/vex/vcc.html
#
#
# Example Output from vcc:
#
# $ vcc --list-context-json
# [
#        "surface",
#        "displace",
#        "light",
#        ...
#        ]
#

#
# $ vcc --list-context-json sop
#
# {
#  "context": "Sop",
#  "globals": {
#            "P": {
#                "type": "vector",
#                "read": true,
#                "write": true
#                },
#            ...},
#  "functions": {
#            "sin": [
#                {
#                    "args": [ "const float"],
#                    "return": "float"
#                    },
#                {
#                    "args": [ "const vector4"],
#                    "return": "vector4"
#                    },
#                {
#                    "args": [ "const vector2"],
#                    "return": "vector2"
#                    },
#                {
#                    "args": [ "const vector"],
#                    "return": "vector"
#                    }
#                ],
#            ...
#            },
#

contextNames = json.loads(subprocess.check_output(["vcc", "--list-context-json"]))
# contextNames = ["cvex"]
 
# Build a dictionary of keys that match the completion. The value for each
# key is an array of items that match it (the variations).
# The VEX context should be part of it.

# Generate a dictionary that makes it easy to implement the omnifunc completer.
# call add(res, { 'word': m, 'menu': 'void(int[] points, vector direction)', 'kind': 'f' })
# let sin = [{'word': 'sin', 'kind': 'f', 'menu': 'float sin(float angle)', 'dup': 1}, {'word': 'sin', 'kind': 'f', 'menu': 'double sin(double angle)', 'dup': 1, }]

print('"')
print('" DO NOT EDIT')
print('" This file is generated by generate-omnifunc-dictionary.py')
print('"')
print("")
print("fun! vex#omnifuncdata#Load() abort")  
print("")
print("let contexts = {}")
print("")
for contextName in contextNames:
    context = json.loads(subprocess.check_output(["vcc", "--list-context-json", contextName]))
    print('" CONTEXT: %s ' % (contextName))
    print("let c = {}")
    for key, value in context["globals"].items():
        print("let c['%s'] = [{'word':'%s','kind':'v','menu':'%s'}]" %(key, key, value["type"]))
    for key, value, in context["functions"].items():
        print("let f = []")
        for variation in value:
            funcDecl = variation["return"] + "(" + ",".join(variation["args"]) + ")"
            print("call add(f,{'word':'%s','kind':'f','menu':'%s'})" %(key, funcDecl))
        print("let c['%s'] = f" % (key))
    print("let contexts['%s'] = c" % (contextName))
print("")
print("return contexts")
print("endfun")

