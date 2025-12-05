from mcp.server.fastmcp import FastMCP
from src.helper import fetch_naukri_jobs,fetch_linkedin_jobs

mcp=FastMCP("Jbot-Recommendation-System",port=8080)

@mcp.tool()
async def fetchlinkedin(listofkey):
    return fetch_linkedin_jobs(query=listofkey,location="",limit=60)
@mcp.tool()
async def fetchnaukri(listofkey):
    return fetch_naukri_jobs(query=listofkey,location="",limit=60)

if __name__ == "__main__":
    mcp.start(transport='stdio')