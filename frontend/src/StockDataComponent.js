import React, { useState, useEffect } from 'react';

const StockDataComponent = ({ symbol }) => {
  const [stockData, setStockData] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      const response = await fetch(`/api/stock?symbol=${symbol}`);
      const data = await response.json();
      setStockData(data);
    };

    fetchData();
  }, [symbol]);



  return (
    <div>
      {}
    </div>
  );
};

export default StockDataComponent;
