from mcp.server.fastmcp import FastMCP
from tools.get_transcript import get_transcript
from tools.generate_summary import generate_summary

mcp = FastMCP("Meeting_Summary")

@mcp.tool()
def summarize(room_id: str) -> dict:
    """Summarizes the transcript of a meeting and returns the summary."""
    transcript = get_transcript(room_id)
    summary = generate_summary(transcript)
    return summary

if __name__ == "__main__":
    mcp.run(transport="stdio")