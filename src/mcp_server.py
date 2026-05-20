from fastmcp import FastMCP

"""
Example of an MCP server using https://github.com/modelcontextprotocol/python-sdk
"""


from fastmcp.dependencies import Depends

from src.energy_system import EnergyFlows, EnumDemandItem, open_session

# Create an MCP server
mcp = FastMCP(
    "MCP supporting LLM-based interaction with the local renewable energy system.",
)


@mcp.tool()
def current_energy_flows(db=Depends(open_session)) -> EnergyFlows:
    """Provides the current status of the energy flows in the local energy system.
    This is meant to provide you with an overview of what is going on here and now
    """
    return EnergyFlows.load_from_database(db)


@mcp.tool()
def stop_demand_item(d: EnumDemandItem, db=Depends(open_session)) -> str:
    """Stops the demand corresponding to the input demand item. This reduces the energy demand."""
    x = EnergyFlows.load_from_database(db)
    x.switch_off(d)
    x.save_to_database(db)
    return f"ok, the {d.value} was stopped"


@mcp.tool()
def start_demand_item(d: EnumDemandItem, db=Depends(open_session)) -> str:
    """Starts the demand corresponding to the input demand item. This increases the energy demand."""
    x = EnergyFlows.load_from_database(db)
    x.switch_on(d)
    x.save_to_database(db)
    return f"ok, the {d.value} was started"


# Run with streamable HTTP transport
if __name__ == "__main__":
    mcp.run(transport="streamable-http")
