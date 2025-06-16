response = {
    "success": True,
    "response": {"insuffficient_context": "need more context", 1: "check"},
}
response = response["response"]
print(response)
if "insuffficient_context" in response:
    print("haaa")
elif 1 in response:
    print("1111")
else:
    print("naaa")    


from random import randint

print(randint(0, 4))