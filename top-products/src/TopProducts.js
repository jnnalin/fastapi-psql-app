// src/TopProducts.js
import './TopProducts.css';
import React, { useEffect, useState } from 'react';
import axios from 'axios';

const TopProducts = () => {
  const [data, setData] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.put('http://localhost:8001/database/custom/top-product');
        setData(response.data.data);
      } catch (err) {
        setError(err.message);
      }
    };

    fetchData();
  }, []);

  if (error) {
    return <div>Error: {error}</div>;
  }

  return (
    <div>
      <h1>Top Products by Category</h1>
      <table>
        <thead>
          <tr>
            <th>Category</th>
            <th>Total Revenue</th>
            <th>Top Product</th>
            <th>Quantity Sold</th>
          </tr>
        </thead>
        <tbody>
          {data.map((item, index) => (
            <tr key={index}>
              <td>{item.category}</td>
              <td>{item.total_revenue}</td>
              <td>{item.top_product}</td>
              <td>{item.top_product_quantity_sold}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default TopProducts;