import LoginButton from './LoginButton';

export default function SignInPage() {
  return (
    <div className='flex items-center justify-center min-h-screen bg-gray-100'>
      <div className='p-6 bg-white rounded-lg shadow-md'>
        <h1 className='mb-4 text-2xl font-bold text-center'>Welcome</h1>
        <LoginButton />
      </div>
    </div>
  );
}
