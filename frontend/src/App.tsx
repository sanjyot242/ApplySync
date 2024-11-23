import Dashboard from './components/Dashboard';
import SignInPage from './components/signInPage';
import { Routes, Route, useNavigate } from 'react-router-dom';
import { useEffect, useState } from 'react';

export default function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    // Check login status when the component mounts
    const checkLoginStatus = () => {
      const loggedInStatus = localStorage.getItem('isAuthenticated') === 'true';
      setIsLoggedIn(loggedInStatus);

      // Use React Router's navigate method to prevent a full reload
      if (loggedInStatus) {
        navigate('/dashboard');
      }
    };

    checkLoginStatus();
  }, [navigate]);

  return (
    <Routes>
      <Route path='/' element={<SignInPage />} />
      <Route
        path='/dashboard'
        element={isLoggedIn ? <Dashboard /> : <SignInPage />}
      />
    </Routes>
  );
}
