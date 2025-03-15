import { NextRequest, NextResponse } from 'next/server';
import { getUserIdentifier, SelfBackendVerifier, countryCodes } from '@selfxyz/core';
import { forbidden } from 'next/navigation';

export async function POST(req: NextRequest) {
  try {

    const body = await req.json();
    const { proof, publicSignals } = body;

    if (!proof || !publicSignals) {
      return NextResponse.json(
        { message: 'Proof and publicSignals are required' },
        { status: 400 }
      );
    }

    // Extract user ID from the proof
    const userId = await getUserIdentifier(publicSignals);
    console.log("Extracted userId:", userId);

    // Initialize and configure the verifier
    const selfBackendVerifier = new SelfBackendVerifier(
      'https://forno.celo.org',
      'Swiish'
    );
    
    // Verify the proof
    const result = await selfBackendVerifier.verify(proof, publicSignals);
    console.log("result ", result)
    if (result.isValid) {
      const country = result.credentialSubject.nationality ?? ''
      const passportNumber = result.credentialSubject.passport_number ?? ''
      const formData = new FormData();
      formData.append('country', country);
      formData.append('passport_number', passportNumber);
      formData.append('user_id', userId);
      const response = await fetch( "https://swiish.money/create-login/", {
        method: 'POST',
        body: formData
      })
      return NextResponse.json({
        status: 'success',
        result: true,
        credentialSubject: result.credentialSubject
      });
    } else {
      return NextResponse.json({
        status: 'error',
        result: false,
        message: 'Verification failed',
        details: result.isValidDetails
      }, { status: 400 });
    }
  } catch (error) {
    console.error('Error verifying proof:', error);
    return NextResponse.json({
      status: 'error',
      result: false,
      message: error instanceof Error ? error.message : 'Unknown error'
    }, { status: 500 });
  }
}