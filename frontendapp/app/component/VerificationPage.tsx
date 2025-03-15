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
    appName: "Swiish",
    scope: "Swiish",
    endpoint: "https://login.swiish.money/api/login",
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

      <p>Scan this QR code with the self.xyz app to login on Swiish</p>
      
      <SelfQRcodeWrapper
        selfApp={selfApp}
        onSuccess={() => {
          try {
            console.log("user uuid ", userId);

            router.push('https://swiish.money/login?user_uuid=' + userId);
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