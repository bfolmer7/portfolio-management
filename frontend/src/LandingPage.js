import React from 'react';
import { Box, Button, Typography, Container, Paper } from '@mui/material';
import { Link } from 'react-router-dom';
import './LandingPage.css'; 

const LandingPage = () => {
  return (
    <Container component="main" maxWidth="xs" className="landing">
      <Paper elevation={6} className="paper">
        <Typography component="h1" variant="h5">
          Welcome to My Portfolio Manager
        </Typography>
        <Box className="box">
          <Typography variant="body1" gutterBottom>
            Your personal assistant for investment management and analysis.
          </Typography>
          <Button
            variant="contained"
            color="primary"
            component={Link}
            to="/login"
            className="loginButton"
          >
            Log In
          </Button>
        </Box>
      </Paper>
    </Container>
  );
};

export default LandingPage;
