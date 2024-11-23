import { useState, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { useToast } from '@/hooks/use-toast';
import axios from 'axios';

export default function Dashboard() {
  const [isServiceRunning, setIsServiceRunning] = useState(false);
  const [sheetData, setSheetData] = useState<string[][]>([]);
  const { toast } = useToast();

  // useEffect(() => {
  //   const fetchSheetData = async () => {
  //     const response = await fetch('/api/sheet');
  //     const data = await response.json();
  //     setSheetData(data);
  //   };

  //   fetchSheetData();
  //   const interval = setInterval(fetchSheetData, 5000); // Update every 5 seconds

  //   return () => clearInterval(interval);
  // }, []);

  const toggleService = async () => {
    const action = isServiceRunning ? 'stop' : 'start';
    const response = await axios.post(
      `http://localhost:5000/api/service/${action}`
    );

    if (response.status === 200) {
      setIsServiceRunning(!isServiceRunning);
      toast({
        title: `Service ${action}ed`,
        description: `The service has been ${action}ed successfully.`,
      });
    } else {
      toast({
        title: 'Error',
        description: `Failed to ${action} the service.`,
        variant: 'destructive',
      });
    }
  };

  return (
    <div className='p-6'>
      <div className='flex justify-between items-center mb-6'>
        <h1 className='text-2xl font-bold'>Dashboard</h1>
        <div className='space-x-4'>
          <Button onClick={toggleService}>
            {isServiceRunning ? 'Stop Service' : 'Start Service'}
          </Button>
          <Button variant='outline' onClick={() => console.log('SignOut')}>
            Sign Out
          </Button>
        </div>
      </div>
      <div className='bg-white p-4 rounded-lg shadow'>
        <h2 className='text-xl font-semibold mb-4'>Google Sheet Data</h2>
        <div className='overflow-x-auto'>
          <table className='min-w-full divide-y divide-gray-200'>
            <thead className='bg-gray-50'>
              <tr>
                {sheetData[0]?.map((header, index) => (
                  <th
                    key={index}
                    className='px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider'>
                    {header}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody className='bg-white divide-y divide-gray-200'>
              {sheetData.slice(1).map((row, rowIndex) => (
                <tr key={rowIndex}>
                  {row.map((cell, cellIndex) => (
                    <td
                      key={cellIndex}
                      className='px-6 py-4 whitespace-nowrap text-sm text-gray-500'>
                      {cell}
                    </td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
