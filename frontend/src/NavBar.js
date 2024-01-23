import React from 'react';
import { Tab, Tabs } from '@mui/material';

const NavBar = () => {
  const [value, setValue] = React.useState(0);

  const handleChange = (event, newValue) => {
    setValue(newValue);
  };

  return (
    <Tabs value={value} onChange={handleChange}>
      <Tab label="Summary" />
      <Tab label="Performance & Risk" />
      {}
    </Tabs>
  );
};

export default NavBar;
