from fastapi import FastAPI, HTTPException, Query
from typing import List, Optional
from .crud import get_top_products, get_channel_activity, search_messages
from .schemas import TopProduct, ChannelActivityDaily, ChannelActivityWeekly, MessageSearchResult

app = FastAPI(title="Medical Insights Analytical API")

@app.get("/api/reports/top-products", response_model=List[TopProduct])
def top_products(limit: int = 10):
    """Get top products by mention count."""
    try:
        products = get_top_products(limit)
        if not products:
            raise HTTPException(status_code=404, detail="No products found.")
        return products
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/channels/{channel_name}/activity", response_model=List[ChannelActivityDaily])
def channel_activity_daily(channel_name: str, period: Optional[str] = Query("daily", enum=["daily", "weekly"])):
    """Get daily or weekly posting trends for a channel."""
    try:
        data = get_channel_activity(channel_name, period)
        if not data:
            raise HTTPException(status_code=404, detail="No activity found for this channel.")
        if period == "weekly":
            # Use weekly response model
            return [ChannelActivityWeekly(**row) for row in data]
        else:
            return [ChannelActivityDaily(**row) for row in data]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/search/messages", response_model=List[MessageSearchResult])
def search_messages_endpoint(query: str):
    """Search messages by keyword."""
    try:
        results = search_messages(query)
        if not results:
            raise HTTPException(status_code=404, detail="No messages found for this query.")
        return [MessageSearchResult(**row) for row in results]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 