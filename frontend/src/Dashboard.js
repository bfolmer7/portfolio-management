import React from 'react';
import NavBar from './NavBar';
import Chart from './Chart';
import './Dashboard.css';

const Dashboard = () => {
  return (
    <div className="dashboard">
      <NavBar />
      <h1>Equity Demo Portfolio Name</h1>
      <Chart />
    </div>
  );
};

export default Dashboard;
