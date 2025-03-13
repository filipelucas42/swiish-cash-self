'use client';
import Image from "next/image";
import dynamic from "next/dynamic";
const VerificationPage = dynamic(
  () => import('./component/VerificationPage'),
  { ssr: false } // This will disable server-side rendering for this component
);
export default function Home() {
  return (
    <VerificationPage />
  );
}
