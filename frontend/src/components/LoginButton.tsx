import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { useEffect, useState } from 'react';
import axios from 'axios';

export default function LoginButton() {
  useEffect(() => {
    // Check login status when the component mounts
    const checkLoginStatus = () => {
      const loggedInStatus = localStorage.getItem('isLoggedIn') === 'true';
      if (loggedInStatus) {
        window.location.href = '/dashboard';
      }
    };

    checkLoginStatus();
  }, []);
  const [email, setEmail] = useState('');

  function inputChangeHandler(event: React.ChangeEvent<HTMLInputElement>) {
    setEmail(event.target.value);
  }

  const signIn = async (email_entered: string) => {
    try {
      const res = await axios.get(
        `http://localhost:5000/api/oauth/google?email=${email_entered}`
      );
      if (res.status === 200) {
        window.location.href = '/dashboard';
        console.log('Sign in successful');
        localStorage.setItem('isAuthenticated', 'true');
      }
    } catch (err) {
      console.log(err);
    }
  };

  return (
    <>
      <Input
        type='email'
        placeholder='Email'
        onChange={inputChangeHandler}
        value={email}
      />
      <Button onClick={() => signIn(email)}>Sign in with Google</Button>
    </>
  );
}
