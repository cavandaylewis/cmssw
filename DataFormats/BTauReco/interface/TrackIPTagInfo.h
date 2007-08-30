#ifndef BTauReco_TrackIpTagInfo_h
#define BTauReco_TrackIpTagInfo_h

#include "DataFormats/BTauReco/interface/RefMacros.h"
#include "DataFormats/GeometryCommonDetAlgo/interface/Measurement1D.h"
#include "DataFormats/TrackReco/interface/TrackFwd.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "DataFormats/BTauReco/interface/JetTracksAssociation.h"
#include "DataFormats/BTauReco/interface/JTATagInfo.h"

namespace reco {
 
class TrackIPTagInfo : public JTATagInfo
 {
  public:

 TrackIPTagInfo(
    std::vector<Measurement1D> ip2d,
   std::vector<Measurement1D> ip3d,
   std::vector<Measurement1D> decayLen,
   std::vector<Measurement1D> jetDistance,
   std::vector<float> prob2d,
   std::vector<float> prob3d,
   edm::RefVector<TrackCollection> selectedTracks,const JetTracksAssociationRef & jtaRef,
   const edm::Ref<VertexCollection> & pv) : JTATagInfo(jtaRef),
     m_ip2d(ip2d),  m_ip3d(ip3d),  m_decayLen(decayLen),
     m_jetDistance(jetDistance),  m_prob2d(prob2d),
     m_prob3d(prob3d), m_selectedTracks(selectedTracks), m_pv(pv) {}

  TrackIPTagInfo() {}
  
  virtual ~TrackIPTagInfo() {}
  
 /**
   Check if probability information is globally available 
   impact parameters in the collection

   Even if true for some tracks it is possible that a -1 probability is returned 
   if some problem occured
  */

  virtual bool hasProbabilities() const { return  m_ip3d.size()==m_prob3d.size(); }
  
  /**
   Vectors of IPs measurement1D orderd as the tracks()
   ip = 0   means 3D
   ip = 1   means transverse IP 
   */
  const std::vector<Measurement1D> & impactParameters(int ip) const {return (ip==0)?m_ip3d:m_ip2d; }
  const std::vector<Measurement1D> & decayLengths() const {return m_decayLen; }
  const std::vector<Measurement1D> & jetDistances() const {return m_jetDistance; }

  const edm::RefVector<TrackCollection> & selectedTracks() const { return m_selectedTracks; }
  const std::vector<float> & probabilities(int ip) const {return (ip==0)?m_prob3d:m_prob2d; }

  typedef enum {IP3DSig = 0, Prob3D = 1, IP2DSig = 2, Prob2D =3 , 
                IP3DValue =4, IP2DValue=5 } SortCriteria;

  /**
   Return the list of track index sorted by mode
   A cut can is specified to select only tracks with
   IP value or significance > cut 
   or
   probability < cut
   (according to the specified mode)
  */
  std::vector<size_t> sortedIndexesWithCut(float cut, SortCriteria mode = IP3DSig) const;

  /**
   Return the list of track index sorted by mode
  */ 
  std::vector<size_t> sortedIndexes(SortCriteria mode = IP3DSig) const;

  reco::TrackRefVector tracks(std::vector<size_t> indexes) const;

  virtual TaggingVariableList taggingVariables(void) const; 
   
   private:
   std::vector<Measurement1D> m_ip2d;   
   std::vector<Measurement1D> m_ip3d;   
   std::vector<Measurement1D> m_decayLen;
   std::vector<Measurement1D> m_jetDistance;
   std::vector<float> m_prob2d;   
   std::vector<float> m_prob3d;   
   edm::RefVector<TrackCollection> m_selectedTracks;
   edm::Ref<VertexCollection> m_pv;

};

//typedef edm::ExtCollection< TrackIPTagInfo,JetTagCollection> TrackCountingExtCollection;
//typedef edm::OneToOneAssociation<JetTagCollection, TrackIPTagInfo> TrackCountingExtCollection;

DECLARE_EDM_REFS( TrackIPTagInfo )

}

#endif
