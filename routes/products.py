from database.session import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from models import CProduct
from sqlalchemy import select, func, desc, cast, Numeric

product_router = APIRouter(prefix="/products")

@product_router.get(
    "/top-product",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "model": dict,
            "description": "Internal server error",
        },
    },
    summary="Finds the top product in each category",
    description="Finds the top product in each category based on the quantity sold.",
    tags=["db"],
)
async def get_top_products(db: AsyncSession = Depends(get_db)):
    try:
        # get the top product in each category
        top_product_subquery = (
            select(
                CProduct.category,
                CProduct.product_name.label('top_product'),
                CProduct.quantity_sold.label('top_product_quantity_sold')
            )
            .order_by(CProduct.category, desc(CProduct.quantity_sold))
            .distinct(CProduct.category)
            .subquery()
        )

        # get the total revenue for each category and join wiht product info
        query = (
            select(
                CProduct.category,
                func.round(cast(func.sum(CProduct.price * CProduct.quantity_sold),Numeric)).label('total_revenue'),
                top_product_subquery.c.top_product,
                top_product_subquery.c.top_product_quantity_sold
            )
            .join(top_product_subquery, CProduct.category == top_product_subquery.c.category)
            .group_by(CProduct.category, top_product_subquery.c.top_product, top_product_subquery.c.top_product_quantity_sold)
        )

        results = await db.execute(query)
        rows = results.fetchall()

        # Convert the rows to a list of dictionaries
        data = [
            {
                "category": row.category,
                "total_revenue": row.total_revenue,
                "top_product": row.top_product,
                "top_product_quantity_sold": row.top_product_quantity_sold,
            }
            for row in rows
        ]

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )

    return {"data": data}