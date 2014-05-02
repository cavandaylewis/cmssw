#! /usr/bin/env python

import ROOT
import sys
from DataFormats.FWLite import Events, Handle

files = ["patTuple_tlbsm_train.root"]
printGen = True
events = Events (files)
handle0  = Handle ("std::vector<pat::Jet>")
handle1  = Handle ("std::vector<pat::Jet>")
handle2  = Handle ("std::vector<pat::Jet>")
handle3  = Handle ("std::vector<pat::Jet>")
handle4  = Handle ("std::vector<pat::Muon>")
handle5  = Handle ("std::vector<pat::Electron>")

# for now, label is just a tuple of strings that is initialized just
# like and edm::InputTag
label0 = ("goodPatJets")
label1 = ("goodPatJetsCA8PrunedPacked")
label2 = ("goodPatJetsCA8CMSTopTagPacked")
label3 = ("goodPatJetsCA15HEPTopTagPacked")
label4 = ("selectedPatMuons")
label5 = ("selectedPatElectrons")

f = ROOT.TFile("outplots.root", "RECREATE")
f.cd()


# loop over events
i = 0
for event in events:
    i = i + 1
    print  '--------- Processing Event ' + str(i)

    print '---- ' + label0
    # use getByLabel, just like in cmsRun
    event.getByLabel (label0, handle0)
    # get the product
    jets0 = handle0.product()


    ijet = 0
    for jet in jets0 :
        print ("Jet {0:4.0f}, pt = {1:10.2f}, eta = {2:6.2f}, phi = {3:6.2f}, m = {4:6.2f}, " +
               "nda = {5:3.0f}, vtxmass = {6:6.2f}, area = {7:6.2f}, L1 = {8:6.2f}, L2 = {9:6.2f}, L3 = {10:6.2f}, " +
               "currLevel = {11:s}").format(
            ijet, jet.pt(), jet.eta(), jet.phi(), jet.mass(), jet.numberOfDaughters(), jet.userFloat('secvtxMass'),
            jet.jetArea(), jet.jecFactor("L1FastJet"), jet.jecFactor("L2Relative"), jet.jecFactor("L3Absolute"), jet.currentJECLevel()
            ),
        if printGen :
            genPt = 0.
            if jet.genJetFwdRef().isNonnull() and jet.genJetFwdRef().isAvailable() :
                genPt = jet.genJetFwdRef().pt()
            else :
                genPt = -1.0
            print (", gen pt = {0:6.2f}").format( genPt )
        else :
            print ''
        ijet += 1
    
    print '---- ' + label1
    # use getByLabel, just like in cmsRun
    event.getByLabel (label1, handle1)
    # get the product
    jets1 = handle1.product()

    ijet = 0
    for jet in jets1 :
        print 'Jet {0:4.0f}, pt = {1:10.2f}, eta = {2:6.2f}, phi = {3:6.2f}, m = {4:6.2f}, nda = {5:3.0f}'.format(
            ijet, jet.pt(), jet.eta(), jet.phi(), jet.mass(), jet.numberOfDaughters()
            ),
        if jet.numberOfDaughters() > 1 :
            print ', ptda1 = {0:6.2f}, ptda1 = {1:6.2f}'.format( jet.daughter(0).pt(), jet.daughter(1).pt() )
        else :
            print ''
        ijet += 1


    print '---- ' + label2
    # use getByLabel, just like in cmsRun
    event.getByLabel (label2, handle2)
    # get the product
    jets2 = handle2.product()

    ijet = 0
    for jet in jets2 :
        print 'Jet {0:4.0f}, pt = {1:10.2f}, eta = {2:6.2f}, phi = {3:6.2f}, m = {4:6.2f}, nda = {5:3.0f}, topmass = {6:6.2f}, minmass = {7:6.2f}'.format(
            ijet, jet.pt(), jet.eta(), jet.phi(), jet.mass(), jet.numberOfDaughters(), jet.tagInfo('CATop').properties().topMass, jet.tagInfo('CATop').properties().minMass
            )
        ijet += 1

        
    print '---- ' + label3
    # use getByLabel, just like in cmsRun
    event.getByLabel (label3, handle3)
    # get the product
    jets3 = handle3.product()

    ijet = 0
    for jet in jets3 :
        print 'Jet {0:4.0f}, pt = {1:10.2f}, eta = {2:6.2f}, phi = {3:6.2f}, m = {4:6.2f}, nda = {5:3.0f}'.format(
            ijet, jet.pt(), jet.eta(), jet.phi(), jet.mass(), jet.numberOfDaughters()
            ),
        if jet.numberOfDaughters() > 2 :
            print ', ptda1 = {0:6.2f}, ptda1 = {1:6.2f}, ptda2 = {2:6.2f}'.format( jet.daughter(0).pt(), jet.daughter(1).pt(), jet.daughter(2).pt() )
        else :
            print ''
        ijet += 1


    print '---- ' + label4
    # use getByLabel, just like in cmsRun
    event.getByLabel (label4, handle4)
    # get the product
    muons1 = handle4.product()

    imuon = 0
    for muon in muons1 :
        if not muon.isGlobalMuon() :
            continue
        print 'Muon {0:4.0f}, pt = {1:10.2f}, eta = {2:6.2f}, phi = {3:6.2f}, m = {4:6.2f}, nda = {5:3.0f}, chi2/dof = {6:6.2f}'.format(
            imuon, muon.pt(), muon.eta(), muon.phi(), muon.mass(), muon.numberOfDaughters(), muon.normChi2()
            )
        imuon += 1

    print '---- ' + label5
    # use getByLabel, just like in cmsRun
    event.getByLabel (label5, handle5)
    # get the product
    electrons1 = handle5.product()

    ielectron = 0
    for electron in electrons1 :
        print 'Electron {0:4.0f}, pt = {1:10.2f}, eta = {2:6.2f}, phi = {3:6.2f}, m = {4:6.2f}, nda = {5:3.0f}, eidTight = {6:6.2f}'.format(
            ielectron, electron.pt(), electron.eta(), electron.phi(), electron.mass(), electron.numberOfDaughters(), electron.electronID('eidTight')
            )
        ielectron += 1 


f.cd()

f.Close()
