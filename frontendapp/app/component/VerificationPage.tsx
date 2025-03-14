'use client';

import React, { useState, useEffect } from 'react';
import SelfQRcodeWrapper, { SelfQRcode, SelfAppBuilder } from '@selfxyz/qrcode';
import { v4 as uuidv4 } from 'uuid';
import { redirect, useRouter } from 'next/navigation';


function VerificationPage() {
  const router = useRouter();
  const [userId, setUserId] = useState<string | null>(null);

  useEffect(() => {
    // Generate a user ID when the component mounts
    setUserId(uuidv4());
  }, []);

  if (!userId) return null;

  // Create the SelfApp configuration
  const selfApp = new SelfAppBuilder({
    appName: "SwiishIt",
    scope: "SwiishIt",
    endpoint: "https://f5dc-64-71-5-91.ngrok-free.app/api/login",
    userId,
    disclosures: {
      // Request passport information
      name: true,
      nationality: true,
      passport_number: true,
    },
  }).build();

  return (
    <div className="verification-container min-h-screen flex flex-col items-center justify-center p-4 bg-white">
        <div className="text-center">
    <img src="/logo_swiish.png" alt="Swiish" style={{ width: '90px', marginTop: '10px', marginBottom: '30px' }} />
  </div>

      <p>Scan this QR code with the Self app to verify your login on swiish app</p>
      
      <SelfQRcodeWrapper
        selfApp={selfApp}
        onSuccess={() => {
          try {
            console.log("user uuid ", userId);

            router.push('http://127.0.0.1:8000/login?user_uuid=' + userId);
          } catch (error) {
            console.error('Navigation error:', error);
          }

        }}
        size={350}
      />
    
    </div>
  );
}

export default VerificationPage;