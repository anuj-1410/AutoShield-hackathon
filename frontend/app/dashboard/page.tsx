"use client"

import { useEffect, useState } from "react"
import { Header } from "@/components/layout/header"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Progress } from "@/components/ui/progress"
import { useWeb3 } from "@/components/providers/web3-provider"
import { Shield, Download, RefreshCw, AlertTriangle, CheckCircle, Clock } from "lucide-react"
import { useToast } from "@/hooks/use-toast"

interface VerificationStatus {
  status: "verified" | "suspected" | "unverified"
  confidence: number
  lastChecked: string
  attestationHash?: string
  riskFactors: string[]
}

export default function DashboardPage() {
  const { account, isConnected } = useWeb3()
  const { toast } = useToast()
  const [verificationStatus, setVerificationStatus] = useState<VerificationStatus | null>(null)
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    if (isConnected && account) {
      fetchVerificationStatus()
    }
  }, [isConnected, account])

  const fetchVerificationStatus = async () => {
    if (!account) return
    
    setLoading(true)
    try {
      // Call real backend API
      const response = await fetch(`http://localhost:8000/api/v1/verification/status/${account}`)
      if (!response.ok) {
        throw new Error('Failed to fetch verification status')
      }
      const data = await response.json()
      
      // Transform backend response to frontend format
      const transformedStatus: VerificationStatus = {
        status: data.status,
        confidence: data.confidence_score,
        lastChecked: data.analyzed_at,
        attestationHash: data.attestation_hash,
        riskFactors: data.risk_factors || [],
      }
      
      setVerificationStatus(transformedStatus)
    } catch (error) {
      console.error('Error fetching verification status:', error)
      toast({
        title: "Error",
        description: "Failed to fetch verification status",
        variant: "destructive",
      })
    } finally {
      setLoading(false)
    }
  }

  const requestReVerification = async () => {
    if (!account) return
    
    setLoading(true)
    try {
      const response = await fetch(`http://localhost:8000/api/v1/verification/analyze`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          wallet_address: account,
          force_refresh: true
        })
      })
      
      if (!response.ok) {
        throw new Error('Failed to request re-verification')
      }
      
      toast({
        title: "Re-verification Completed",
        description: "Your account has been re-analyzed successfully.",
      })
      
      // Fetch updated status
      await fetchVerificationStatus()
    } catch (error) {
      console.error('Error requesting re-verification:', error)
      toast({
        title: "Error",
        description: "Failed to request re-verification",
        variant: "destructive",
      })
    } finally {
      setLoading(false)
    }
  }

  const downloadAttestation = () => {
    const attestationData = {
      address: account,
      status: verificationStatus?.status,
      timestamp: verificationStatus?.lastChecked,
      hash: verificationStatus?.attestationHash,
    }

    const blob = new Blob([JSON.stringify(attestationData, null, 2)], { type: "application/json" })
    const url = URL.createObjectURL(blob)
    const a = document.createElement("a")
    a.href = url
    a.download = `autoshield-attestation-${account?.slice(0, 8)}.json`
    a.click()
    URL.revokeObjectURL(url)
  }

  if (!isConnected) {
    return (
      <div className="min-h-screen bg-background">
        <Header />
        <div className="container mx-auto px-4 py-16">
          <Card className="max-w-md mx-auto">
            <CardHeader className="text-center">
              <Shield className="h-12 w-12 mx-auto mb-4 text-primary" />
              <CardTitle>Connect Your Wallet</CardTitle>
              <CardDescription>Please connect your wallet to view your verification status</CardDescription>
            </CardHeader>
          </Card>
        </div>
      </div>
    )
  }

  const getStatusIcon = (status: string) => {
    switch (status) {
      case "verified":
        return <CheckCircle className="h-5 w-5 text-green-400" />
      case "suspected":
        return <AlertTriangle className="h-5 w-5 text-red-400" />
      default:
        return <Clock className="h-5 w-5 text-yellow-400" />
    }
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case "verified":
        return "verification-verified"
      case "suspected":
        return "verification-suspected"
      default:
        return "verification-unverified"
    }
  }

  return (
    <div className="min-h-screen bg-background">
      <Header />
      <div className="container mx-auto px-4 py-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold mb-2">Account Dashboard</h1>
          <p className="text-muted-foreground">Manage your verification status and download attestations</p>
        </div>

        <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
          {/* Verification Status Card */}
          <Card className="md:col-span-2">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Shield className="h-5 w-5" />
                Verification Status
              </CardTitle>
              <CardDescription>
                Current verification status for {account?.slice(0, 6)}...{account?.slice(-4)}
              </CardDescription>
            </CardHeader>
            <CardContent>
              {loading ? (
                <div className="space-y-4">
                  <div className="h-4 bg-muted rounded animate-pulse" />
                  <div className="h-4 bg-muted rounded animate-pulse w-3/4" />
                  <div className="h-4 bg-muted rounded animate-pulse w-1/2" />
                </div>
              ) : verificationStatus ? (
                <div className="space-y-4">
                  <div className="flex items-center gap-2">
                    {getStatusIcon(verificationStatus.status)}
                    <Badge className={getStatusColor(verificationStatus.status)}>
                      {verificationStatus.status.toUpperCase()}
                    </Badge>
                    <span className="text-sm text-muted-foreground">{verificationStatus.confidence}% confidence</span>
                  </div>

                  <div>
                    <div className="flex justify-between text-sm mb-2">
                      <span>Verification Score</span>
                      <span>{verificationStatus.confidence}%</span>
                    </div>
                    <Progress value={verificationStatus.confidence} className="h-2" />
                  </div>

                  <div className="text-sm text-muted-foreground">
                    Last checked: {new Date(verificationStatus.lastChecked).toLocaleString()}
                  </div>

                  {verificationStatus.riskFactors.length > 0 && (
                    <div>
                      <h4 className="font-medium mb-2 text-red-400">Risk Factors:</h4>
                      <ul className="text-sm space-y-1">
                        {verificationStatus.riskFactors.map((factor, index) => (
                          <li key={index} className="flex items-center gap-2">
                            <AlertTriangle className="h-3 w-3 text-red-400" />
                            {factor}
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}

                  <div className="flex gap-2 pt-4">
                    <Button onClick={requestReVerification} disabled={loading}>
                      <RefreshCw className="h-4 w-4 mr-2" />
                      Request Re-verification
                    </Button>
                    {verificationStatus.attestationHash && (
                      <Button variant="outline" onClick={downloadAttestation}>
                        <Download className="h-4 w-4 mr-2" />
                        Download Attestation
                      </Button>
                    )}
                  </div>
                </div>
              ) : null}
            </CardContent>
          </Card>

          {/* Quick Stats */}
          <Card>
            <CardHeader>
              <CardTitle>Account Info</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div>
                <div className="text-sm text-muted-foreground">Wallet Address</div>
                <div className="font-mono text-sm">
                  {account?.slice(0, 6)}...{account?.slice(-4)}
                </div>
              </div>
              <div>
                <div className="text-sm text-muted-foreground">Network</div>
                <div className="text-sm">Ethereum Mainnet</div>
              </div>
              <div>
                <div className="text-sm text-muted-foreground">Member Since</div>
                <div className="text-sm">January 2024</div>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Recent Activity */}
        <Card className="mt-6">
          <CardHeader>
            <CardTitle>Recent Activity</CardTitle>
            <CardDescription>Your recent verification and attestation history</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {[
                { action: "Verification completed", time: "2 hours ago", status: "success" },
                { action: "Attestation generated", time: "2 hours ago", status: "success" },
                { action: "Account connected", time: "1 day ago", status: "info" },
              ].map((activity, index) => (
                <div
                  key={index}
                  className="flex items-center justify-between py-2 border-b border-border last:border-0"
                >
                  <div>
                    <div className="font-medium">{activity.action}</div>
                    <div className="text-sm text-muted-foreground">{activity.time}</div>
                  </div>
                  <Badge variant={activity.status === "success" ? "default" : "secondary"}>{activity.status}</Badge>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
