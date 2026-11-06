
#### Rules Engine
#index/keyword
#index/glossary -- [[True vs False vs Other]] -- the other is key here for NSF definition
#index/fan-in 

#index/synonym 
#index/synonym/prime -- 
#index/homonym
#index/semantic-collision -- `a x b`, `a x b x c`
#index/semantic-ambiguity -- unknown, need analysis
#index/semantic-ambiguity/soup -- some true, some false
#index/semantic-drift 
#index/friction
#index/pitfall -- what could go wrong
	#index/anti-pattern -- evaluated and confirmed
	#index/pitfall/unfounded -- evaluated and determined false or immaterial -- document threshold
#index/hard-block -- 
#index/whitelist -- selection, inclusion
#index/blacklist -- anti-selection, exclusion
#index/decision-point -- in timestamp block, tag this + `<contact>` and now can have trace
- ⚠️ develop this idea

#index/snapshot
#index/enrichment

#### Pain-Point

#pain-point/lag -- too slow
#pain-point/cost -- too cost
#pain-point/profit -- cost:benefit throughput too low 

#solve/accelerate -- curb time-cost, remove friction 
#solve/amplify -- promote, incentivize benefit
#solve/constrain -- curb cost

#solve/monitor -- deploy telemetry
#solve/spike -- discovery
#solve/spike/diff-analysis -- `a x b`, `a x b x c` 
#solve/spike/delta -- `a x b x t` (before v after)

#### Product

#product/dashboard-agg
#product/report-detail
#product/semantic-model
#product/table-artifact
	#product/source-coupled
	#product/history-governed -- frozen partitions (eg `month-close`)

#product/reasoning-trace
#product/lineage-trace
#product/sequence-trace


#product/change-manifest/on-push -- on build, intended changes
#product/change-manifest/by-snapshot -- full snapshot then delta

#product/canvas-ui

#### Flow

**vertical axis = grain**
#vertical/parent -- #horizontal/parent
#vertical/child -- label, but not a field descriptor. only define parent. child implied
#vertical/orphan -- lost parent
#vertical/vilomah -- lost child

**horizontal axis = time**
#horizontal/predecessor -- ancestor, upstream, source 
#horizontal/successor -- descendant, downstream, target (implied -- field-tag: predecessor)

#cardinality/1-1
#cardinality/1-n

#flow/anti-pattern -- related to 
#flow/pivot-pattern -- retrain bias away from anti to happy-path
#flow/happy-path-pattern

#flow/pattern-a -- c/b pattern-a
#flow/pattern-b -- alternative
#flow/pattern-c
