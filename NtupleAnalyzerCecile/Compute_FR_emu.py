def add_lumi(year):
    lowX=0.4
    lowY=0.835
    lumi  = ROOT.TPaveText(lowX, lowY+0.06, lowX+0.30, lowY+0.16, "NDC")
    lumi.SetBorderSize(   0 )
    lumi.SetFillStyle(    0 )
    lumi.SetTextAlign(   12 )
    lumi.SetTextColor(    1 )
    lumi.SetTextSize(0.055)
    lumi.SetTextFont (   42 )
    if (year=="2018"): lumi.AddText("2018, 60 fb^{-1} (13 TeV)")
    if (year=="2017"): lumi.AddText("2017, 41 fb^{-1} (13 TeV)")
    if (year=="2016"): lumi.AddText("2016, 36 fb^{-1} (13 TeV)")
    return lumi

def add_CMS():
    lowX=0.16
    lowY=0.835
    lumi  = ROOT.TPaveText(lowX, lowY+0.06, lowX+0.15, lowY+0.16, "NDC")
    lumi.SetTextFont(61)
    lumi.SetTextSize(0.065)
    lumi.SetBorderSize(   0 )
    lumi.SetFillStyle(    0 )
    lumi.SetTextAlign(   12 )
    lumi.SetTextColor(    1 )
    lumi.AddText("CMS")
    return lumi


if __name__ == "__main__":

    import ROOT
    import argparse
    ROOT.gStyle.SetOptStat(0)

    parser = argparse.ArgumentParser()
    parser.add_argument('--year', default="2016", choices=['2016', '2017', '2018'], help="Which TES?")

    options = parser.parse_args()
    postfixName=[""]


    fVV=ROOT.TFile("output_emu_"+options.year+"/VV.root","r")
    fTT=ROOT.TFile("output_emu_"+options.year+"/TT.root","r")
    fST=ROOT.TFile("output_emu_"+options.year+"/ST.root","r")
    fDY=ROOT.TFile("output_emu_"+options.year+"/DY.root","r")
    fData=ROOT.TFile("output_emu_"+options.year+"/MuonEG.root","r")
    fout=ROOT.TFile("emu_fr_2018.root","recreate")

    h0iso=fData.Get("h_fr_iso")
    h0iso.Add(fVV.Get("h_fr_iso"),-1)
    h0iso.Add(fDY.Get("h_fr_iso"),-1)
    h0iso.Add(fTT.Get("h_fr_iso"),-1)
    h0iso.Add(fST.Get("h_fr_iso"),-1)

    h0anti=fData.Get("h_fr_anti")
    h0anti.Add(fVV.Get("h_fr_anti"),-1)
    h0anti.Add(fDY.Get("h_fr_anti"),-1)
    h0anti.Add(fTT.Get("h_fr_anti"),-1)
    h0anti.Add(fST.Get("h_fr_anti"),-1)

    h0iso.Divide(h0anti)
    fout.cd()
    h0iso.SetName("FR")
    h0iso.Write()

    h1iso=fData.Get("h_frnt_iso")
    h1iso.Add(fVV.Get("h_frnt_iso"),-1)
    h1iso.Add(fDY.Get("h_frnt_iso"),-1)
    h1iso.Add(fTT.Get("h_frnt_iso"),-1)
    h1iso.Add(fST.Get("h_frnt_iso"),-1)

    h1anti=fData.Get("h_frnt_anti")
    h1anti.Add(fVV.Get("h_frnt_anti"),-1)
    h1anti.Add(fDY.Get("h_frnt_anti"),-1)
    h1anti.Add(fTT.Get("h_frnt_anti"),-1)
    h1anti.Add(fST.Get("h_frnt_anti"),-1)

    h1iso.Divide(h1anti)
    average=h1iso.GetBinContent(1)
    for k in range(1,h1iso.GetSize()):
       h1iso.SetBinContent(k,h1iso.GetBinContent(k)/average)
    fout.cd()
    h1iso.SetName("FRNT")
    h1iso.Write()

    c=ROOT.TCanvas("canvas","",0,0,800,800)
    c.cd()
    h1iso.SetTitle("")
    h1iso.SetMarkerStyle(20)
    h1iso.SetMarkerColor(1)
    h1iso.SetLineColor(1)
    h1iso.GetXaxis().SetTitle("N_{tracks}")
    h1iso.GetYaxis().SetTitle("OS-to-SS ratio / average")
    h1iso.Draw("e0p")
    h1iso.GetXaxis().SetRangeUser(0,100)
    h1iso.SetMinimum(0.5)
    lumi=add_lumi(options.year)
    lumi.Draw("same")
    cms=add_CMS()
    cms.Draw("same")
    total = ROOT.TF1( 'total', 'pol5', 0, 100 )
    total.SetLineColor( 2 )
    h1iso.Fit(total,'R')
    total.SetName("fit_frnt")

    hint = ROOT.TH1D("hint","Fitted Gaussian with .68 conf.band", 100, 0, 100);
    (ROOT.TVirtualFitter.GetFitter()).GetConfidenceIntervals(hint,0.68);
    hint.SetStats(False);
    hint.SetFillColor(ROOT.kCyan);
    hint.SetFillStyle(3001);
    hint.Draw("e3 same");

    fout.cd()
    total.Write()
    c.cd()
    c.Modified()
    c.SaveAs("plots_emu_"+options.year+"/frnt.pdf")
    c.SaveAs("plots_emu_"+options.year+"/frnt.png")

    h0iso.SetTitle("")
    h0iso.SetMarkerStyle(20)
    h0iso.SetMarkerColor(1)
    h0iso.SetLineColor(1)
    h0iso.GetXaxis().SetTitle("p_{T}(e) (GeV)")
    h0iso.GetYaxis().SetTitle("p_{T}(#mu) (GeV)")
    h0iso.GetZaxis().SetTitle("OS/SS ratio")
    h0iso.Draw("colz")
    lumi=add_lumi(options.year)
    lumi.Draw("same")
    cms=add_CMS()
    cms.Draw("same")
    c.cd()
    c.Modified()
    c.SaveAs("plots_emu_"+options.year+"/fr2D.pdf")
    c.SaveAs("plots_emu_"+options.year+"/fr2D.png")


    h2iso=fData.Get("h_frFP_iso")
    h2iso.Add(fVV.Get("h_frFP_iso"),-1)
    h2iso.Add(fDY.Get("h_frFP_iso"),-1)
    h2iso.Add(fTT.Get("h_frFP_iso"),-1)
    h2iso.Add(fST.Get("h_frFP_iso"),-1)
    h2anti=fData.Get("h_frFP_anti")
    h2anti.Add(fVV.Get("h_frFP_anti"),-1)
    h2anti.Add(fDY.Get("h_frFP_anti"),-1)
    h2anti.Add(fTT.Get("h_frFP_anti"),-1)
    h2anti.Add(fST.Get("h_frFP_anti"),-1)
    h2iso.Divide(h2anti)

    h3iso=fData.Get("h_frFF_iso")
    h3iso.Add(fVV.Get("h_frFF_iso"),-1)
    h3iso.Add(fDY.Get("h_frFF_iso"),-1)
    h3iso.Add(fTT.Get("h_frFF_iso"),-1)
    h3iso.Add(fST.Get("h_frFF_iso"),-1)
    h3anti=fData.Get("h_frFF_anti")
    h3anti.Add(fVV.Get("h_frFF_anti"),-1)
    h3anti.Add(fDY.Get("h_frFF_anti"),-1)
    h3anti.Add(fTT.Get("h_frFF_anti"),-1)
    h3anti.Add(fST.Get("h_frFF_anti"),-1)
    h3iso.Divide(h3anti)

    h2iso.Divide(h3iso)
    fout.cd()
    h2iso.SetName("FRantimu")
    h2iso.Write()

    h2iso.SetTitle("")
    h2iso.SetMarkerStyle(20)
    h2iso.SetMarkerColor(1)
    h2iso.SetLineColor(1)
    h2iso.GetXaxis().SetTitle("p_{T}(e) (GeV)")
    h2iso.GetYaxis().SetTitle("p_{T}(#mu) (GeV)")
    h2iso.GetZaxis().SetTitle("anti-#mu correction")
    h2iso.Draw("colz")
    lumi.Draw("same")
    cms.Draw("same")
    c.cd()
    c.Modified()
    c.SaveAs("plots_emu_"+options.year+"/frantimu.pdf")
    c.SaveAs("plots_emu_"+options.year+"/frantimu.png")

