import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { Copy, QrCode } from "lucide-react";
import QRCode from "qrcode";
import { useEffect, useState } from "react";
import { toast } from "sonner";

interface QRCodeModalProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
}

export function QRCodeModal({ open, onOpenChange }: QRCodeModalProps) {
  const [qrCodeDataURL, setQrCodeDataURL] = useState<string>("");
  const [dashboardURL, setDashboardURL] = useState<string>("");

  useEffect(() => {
    if (open) {
      const generateQRCode = async () => {
        try {
          const url = window.location.origin;
          setDashboardURL(url);
          
          const qrDataURL = await QRCode.toDataURL(url, {
            width: 300,
            margin: 2,
            color: {
              dark: "#000000",
              light: "#FFFFFF"
            }
          });
          
          setQrCodeDataURL(qrDataURL);
        } catch (error) {
          console.error("Failed to generate QR code:", error);
          toast.error("Failed to generate QR code");
        }
      };

      generateQRCode();
    }
  }, [open]);

  const copyToClipboard = async () => {
    try {
      await navigator.clipboard.writeText(dashboardURL);
      toast.success("Dashboard URL copied to clipboard");
    } catch (error) {
      console.error("Failed to copy URL:", error);
      toast.error("Failed to copy URL");
    }
  };

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="sm:max-w-md">
        <DialogHeader>
          <DialogTitle className="flex items-center gap-2">
            <QrCode className="size-5 text-blue-500" />
            iPad Access QR Code
          </DialogTitle>
        </DialogHeader>
        
        <div className="flex flex-col items-center space-y-4">
          {qrCodeDataURL ? (
            <div className="bg-white p-4 rounded-lg border">
              <img 
                src={qrCodeDataURL} 
                alt="QR Code for Dashboard Access" 
                className="w-[300px] h-[300px]"
              />
            </div>
          ) : (
            <div className="w-[300px] h-[300px] bg-gray-100 rounded-lg flex items-center justify-center">
              <div className="text-center">
                <QrCode className="size-8 mx-auto mb-2 text-gray-400" />
                <p className="text-sm text-gray-500">Generating QR code...</p>
              </div>
            </div>
          )}
          
          <div className="text-center space-y-2">
            <p className="text-sm font-medium">
              Students can scan this QR code with their iPad camera
            </p>
            <p className="text-xs text-muted-foreground">
              This will open the dashboard directly on their device
            </p>
          </div>
          
          <div className="w-full bg-gray-50 rounded-lg p-3">
            <p className="text-xs text-muted-foreground mb-1">Dashboard URL:</p>
            <p className="text-sm font-mono break-all">{dashboardURL}</p>
          </div>
        </div>

        <DialogFooter className="gap-2">
          <Button variant="outline" onClick={copyToClipboard}>
            <Copy className="size-4 mr-2" />
            Copy URL
          </Button>
          <Button onClick={() => onOpenChange(false)}>
            Close
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}