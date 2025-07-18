"use client"

import { useState, useEffect } from "react"
import { Header } from "@/components/layout/header"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Progress } from "@/components/ui/progress"
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from "recharts"
import { Users, AlertTriangle, CheckCircle, Download, TrendingUp, Activity } from "lucide-react"

interface AdminStats {
  totalAccounts: number
  verifiedAccounts: number
  suspectedAccounts: number
  unverifiedAccounts: number
  dailyVerifications: number
  falsePositiveRate: number
  systemHealth: number
}

interface FlaggedAccount {
  address: string
  riskScore: number
  flaggedAt: string
  reasons: string[]
  status: "pending" | "reviewed" | "confirmed"
}

export default function AdminPage() {
  const [stats, setStats] = useState<AdminStats | null>(null)
  const [flaggedAccounts, setFlaggedAccounts] = useState<FlaggedAccount[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchAdminData()
  }, [])

  const fetchAdminData = async () => {
    setLoading(true)

    try {
      // Fetch system stats
      const statsResponse = await fetch('http://localhost:8000/api/v1/analytics/system-stats')
      if (!statsResponse.ok) {
        throw new Error('Failed to fetch system stats')
      }
      const statsData = await statsResponse.json()
      
      // Transform backend response
      const transformedStats: AdminStats = {
        totalAccounts: statsData.total_verifications,
        verifiedAccounts: statsData.verified_accounts,
        suspectedAccounts: statsData.suspected_accounts,
        unverifiedAccounts: statsData.unverified_accounts,
        dailyVerifications: 342, // Mock for now
        falsePositiveRate: statsData.false_positive_rate,
        systemHealth: statsData.system_health,
      }

      // Fetch flagged accounts
      const flaggedResponse = await fetch('http://localhost:8000/api/v1/admin/flagged-accounts')
      if (!flaggedResponse.ok) {
        throw new Error('Failed to fetch flagged accounts')
      }
      const flaggedData = await flaggedResponse.json()
      
      // Transform flagged accounts
      const transformedFlagged: FlaggedAccount[] = flaggedData.flagged_accounts.map((acc: any) => ({
        address: acc.wallet_address,
        riskScore: acc.risk_score,
        flaggedAt: acc.flagged_at,
        reasons: acc.reasons,
        status: acc.status,
      }))

      setStats(transformedStats)
      setFlaggedAccounts(transformedFlagged)
    } catch (error) {
      console.error('Error fetching admin data:', error)
      // Fallback to mock data on error
      const mockStats: AdminStats = {
        totalAccounts: 15847,
        verifiedAccounts: 12678,
        suspectedAccounts: 1234,
        unverifiedAccounts: 1935,
        dailyVerifications: 342,
        falsePositiveRate: 2.3,
        systemHealth: 98.5,
      }
      setStats(mockStats)
    } finally {
      setLoading(false)
    }
  }

  const chartData = [
    { name: "Mon", verifications: 45 },
    { name: "Tue", verifications: 52 },
    { name: "Wed", verifications: 38 },
    { name: "Thu", verifications: 61 },
    { name: "Fri", verifications: 55 },
    { name: "Sat", verifications: 42 },
    { name: "Sun", verifications: 48 },
  ]

  const pieData = stats
    ? [
        { name: "Verified", value: stats.verifiedAccounts, color: "#10b981" },
        { name: "Suspected", value: stats.suspectedAccounts, color: "#ef4444" },
        { name: "Unverified", value: stats.unverifiedAccounts, color: "#f59e0b" },
      ]
    : []

  const exportReport = () => {
    const reportData = {
      timestamp: new Date().toISOString(),
      stats,
      flaggedAccounts,
      summary: {
        totalProcessed: stats?.totalAccounts || 0,
        accuracyRate: 100 - (stats?.falsePositiveRate || 0),
        systemHealth: stats?.systemHealth || 0,
      },
    }

    const blob = new Blob([JSON.stringify(reportData, null, 2)], { type: "application/json" })
    const url = URL.createObjectURL(blob)
    const a = document.createElement("a")
    a.href = url
    a.download = `autoshield-admin-report-${new Date().toISOString().split("T")[0]}.json`
    a.click()
    URL.revokeObjectURL(url)
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-background">
        <Header />
        <div className="container mx-auto px-4 py-8">
          <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-4">
            {[...Array(4)].map((_, i) => (
              <Card key={i}>
                <CardContent className="p-6">
                  <div className="h-4 bg-muted rounded animate-pulse mb-2" />
                  <div className="h-8 bg-muted rounded animate-pulse" />
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-background">
      <Header />
      <div className="container mx-auto px-4 py-8">
        <div className="flex justify-between items-center mb-8">
          <div>
            <h1 className="text-3xl font-bold mb-2">Admin Dashboard</h1>
            <p className="text-muted-foreground">Monitor system performance and manage flagged accounts</p>
          </div>
          <Button onClick={exportReport}>
            <Download className="h-4 w-4 mr-2" />
            Export Report
          </Button>
        </div>

        {/* Stats Overview */}
        <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-4 mb-8">
          <Card>
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-muted-foreground">Total Accounts</p>
                  <p className="text-2xl font-bold">{stats?.totalAccounts.toLocaleString()}</p>
                </div>
                <Users className="h-8 w-8 text-primary" />
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-muted-foreground">Verified</p>
                  <p className="text-2xl font-bold text-green-400">{stats?.verifiedAccounts.toLocaleString()}</p>
                </div>
                <CheckCircle className="h-8 w-8 text-green-400" />
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-muted-foreground">Suspected</p>
                  <p className="text-2xl font-bold text-red-400">{stats?.suspectedAccounts.toLocaleString()}</p>
                </div>
                <AlertTriangle className="h-8 w-8 text-red-400" />
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-muted-foreground">System Health</p>
                  <p className="text-2xl font-bold">{stats?.systemHealth}%</p>
                </div>
                <Activity className="h-8 w-8 text-primary" />
              </div>
            </CardContent>
          </Card>
        </div>

        <Tabs defaultValue="overview" className="space-y-6">
          <TabsList>
            <TabsTrigger value="overview">Overview</TabsTrigger>
            <TabsTrigger value="flagged">Flagged Accounts</TabsTrigger>
            <TabsTrigger value="analytics">Analytics</TabsTrigger>
          </TabsList>

          <TabsContent value="overview" className="space-y-6">
            <div className="grid gap-6 md:grid-cols-2">
              <Card>
                <CardHeader>
                  <CardTitle>Daily Verifications</CardTitle>
                  <CardDescription>Number of accounts verified per day this week</CardDescription>
                </CardHeader>
                <CardContent>
                  <ResponsiveContainer width="100%" height={300}>
                    <BarChart data={chartData}>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis dataKey="name" />
                      <YAxis />
                      <Tooltip />
                      <Bar dataKey="verifications" fill="#8b5cf6" />
                    </BarChart>
                  </ResponsiveContainer>
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle>Account Distribution</CardTitle>
                  <CardDescription>Breakdown of account verification statuses</CardDescription>
                </CardHeader>
                <CardContent>
                  <ResponsiveContainer width="100%" height={300}>
                    <PieChart>
                      <Pie
                        data={pieData}
                        cx="50%"
                        cy="50%"
                        outerRadius={80}
                        dataKey="value"
                        label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                      >
                        {pieData.map((entry, index) => (
                          <Cell key={`cell-${index}`} fill={entry.color} />
                        ))}
                      </Pie>
                      <Tooltip />
                    </PieChart>
                  </ResponsiveContainer>
                </CardContent>
              </Card>
            </div>

            <Card>
              <CardHeader>
                <CardTitle>System Performance</CardTitle>
                <CardDescription>Key performance indicators for the AutoShield system</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div>
                  <div className="flex justify-between text-sm mb-2">
                    <span>Accuracy Rate</span>
                    <span>{100 - (stats?.falsePositiveRate || 0)}%</span>
                  </div>
                  <Progress value={100 - (stats?.falsePositiveRate || 0)} className="h-2" />
                </div>
                <div>
                  <div className="flex justify-between text-sm mb-2">
                    <span>System Health</span>
                    <span>{stats?.systemHealth}%</span>
                  </div>
                  <Progress value={stats?.systemHealth} className="h-2" />
                </div>
                <div>
                  <div className="flex justify-between text-sm mb-2">
                    <span>Processing Speed</span>
                    <span>95%</span>
                  </div>
                  <Progress value={95} className="h-2" />
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="flagged" className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle>Flagged Accounts</CardTitle>
                <CardDescription>Accounts that have been flagged by the AI system for review</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {flaggedAccounts.map((account, index) => (
                    <div key={index} className="border rounded-lg p-4">
                      <div className="flex items-center justify-between mb-3">
                        <div className="font-mono text-sm">
                          {account.address.slice(0, 6)}...{account.address.slice(-4)}
                        </div>
                        <div className="flex items-center gap-2">
                          <Badge
                            variant={
                              account.status === "confirmed"
                                ? "destructive"
                                : account.status === "reviewed"
                                  ? "default"
                                  : "secondary"
                            }
                          >
                            {account.status}
                          </Badge>
                          <span className="text-sm text-muted-foreground">Risk: {account.riskScore}%</span>
                        </div>
                      </div>

                      <div className="space-y-2">
                        <div className="text-sm text-muted-foreground">
                          Flagged: {new Date(account.flaggedAt).toLocaleString()}
                        </div>
                        <div>
                          <div className="text-sm font-medium mb-1">Reasons:</div>
                          <ul className="text-sm space-y-1">
                            {account.reasons.map((reason, i) => (
                              <li key={i} className="flex items-center gap-2">
                                <AlertTriangle className="h-3 w-3 text-red-400" />
                                {reason}
                              </li>
                            ))}
                          </ul>
                        </div>
                      </div>

                      {account.status === "pending" && (
                        <div className="flex gap-2 mt-4">
                          <Button size="sm" variant="destructive">
                            Confirm Fake
                          </Button>
                          <Button size="sm" variant="outline">
                            Mark as False Positive
                          </Button>
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="analytics" className="space-y-6">
            <div className="grid gap-6 md:grid-cols-3">
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <TrendingUp className="h-5 w-5" />
                    Detection Rate
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold text-green-400">97.7%</div>
                  <p className="text-sm text-muted-foreground">Successfully detected fake accounts</p>
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle>False Positive Rate</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold text-yellow-400">{stats?.falsePositiveRate}%</div>
                  <p className="text-sm text-muted-foreground">Legitimate accounts flagged as fake</p>
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle>Processing Time</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold">1.2s</div>
                  <p className="text-sm text-muted-foreground">Average verification time</p>
                </CardContent>
              </Card>
            </div>
          </TabsContent>
        </Tabs>
      </div>
    </div>
  )
}
