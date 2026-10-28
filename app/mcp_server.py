"""Optional standalone MCP stdio server using synthetic fixtures."""
from mcp.server.fastmcp import FastMCP
from app.services import get_patient,get_policy
mcp=FastMCP("synthetic-prior-auth")

@mcp.tool()
def patient_by_id(patient_id:str)->dict:
    """Retrieve a synthetic FHIR Patient."""
    return get_patient(patient_id)

@mcp.tool()
def fictional_payer_policy(procedure_code:str)->dict:
    """Retrieve a fictional policy."""
    return get_policy(procedure_code)

if __name__=="__main__": mcp.run(transport="stdio")
