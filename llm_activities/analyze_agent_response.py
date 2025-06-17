"""
"""


def analyze_agent_response(response):
    """
    take actions according to response info returned by agent.
    """

    if "insufficient_context" in response:
        return {
            "type": "insufficient_context",
            "message": response["insufficient_context"],
        }
    elif "greeting" in response:
        return {
            "type": "greeting",
            "message": response["greeting"],
        }
    elif "invalid_query" in response:
        return {
            "type": "invalid_query",
            "message": "OOps the query is out of the context for me. Kindly ask something relevant.",
        }
    elif "llm_failure" in response:
        return {
            "type": "llm_failure",
            "message": "something went wrong!",
        }

    start_time = response["start_time"]
    end_time = response["end_time"]

    return {"start_time": start_time, "end_time": end_time}
