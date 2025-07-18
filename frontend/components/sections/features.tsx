import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Brain, Shield, Users, Zap, Lock, Globe, BarChart3, CheckCircle } from "lucide-react"

const features = [
  {
    icon: Brain,
    title: "Advanced AI Detection",
    description:
      "Machine learning models trained on millions of blockchain transactions to identify suspicious patterns and fake accounts.",
    badge: "AI/ML",
  },
  {
    icon: Shield,
    title: "Blockchain Verification",
    description:
      "Cryptographically signed attestations stored on-chain for transparent and tamper-proof verification results.",
    badge: "Blockchain",
  },
  {
    icon: Users,
    title: "Community Governance",
    description:
      "Decentralized decision-making with community feedback integration and appeal processes for disputed results.",
    badge: "DAO",
  },
  {
    icon: Zap,
    title: "Real-time Processing",
    description: "Sub-second verification with instant results for seamless integration into existing dApp workflows.",
    badge: "Performance",
  },
  {
    icon: Lock,
    title: "Privacy Preserving",
    description: "Zero personal data collection. Only public blockchain data is analyzed with results hashed on-chain.",
    badge: "Privacy",
  },
  {
    icon: Globe,
    title: "Cross-Platform Integration",
    description: "Easy integration with any Web3 platform through REST APIs and smart contract interfaces.",
    badge: "Integration",
  },
  {
    icon: BarChart3,
    title: "Analytics Dashboard",
    description: "Comprehensive analytics and reporting tools for administrators and platform operators.",
    badge: "Analytics",
  },
  {
    icon: CheckCircle,
    title: "Attestation System",
    description: "Downloadable cryptographic proofs of verification status for use across multiple platforms.",
    badge: "Attestation",
  },
]

export function Features() {
  return (
    <section className="py-24 bg-muted/30">
      <div className="container mx-auto px-4">
        <div className="text-center mb-16">
          <h2 className="text-3xl font-bold mb-4">Comprehensive Web3 Security Solution</h2>
          <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
            AutoShield combines cutting-edge AI technology with blockchain transparency to provide the most robust fake
            account detection system for Web3.
          </p>
        </div>

        <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-4">
          {features.map((feature, index) => (
            <Card key={index} className="relative overflow-hidden">
              <CardHeader>
                <div className="flex items-center justify-between mb-2">
                  <feature.icon className="h-8 w-8 text-primary" />
                  <Badge variant="secondary" className="text-xs">
                    {feature.badge}
                  </Badge>
                </div>
                <CardTitle className="text-lg">{feature.title}</CardTitle>
              </CardHeader>
              <CardContent>
                <CardDescription className="text-sm">{feature.description}</CardDescription>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    </section>
  )
}
