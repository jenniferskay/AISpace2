/** Events that can be received from the backend. */

import { Events, IEvent } from "../Events";

export interface ICSPHighlightArcsEvent extends IEvent {
  action: "highlightArcs";
  // The IDs of the arc to highlight. If null, all arcs are highlighted
  arcIds: string[] | null;
  // The thickness of the highlight
  style: "normal" | "bold";
  // The colour of the highlight
  colour: string;
}

export interface ICSPSetDomainsEvent extends IEvent {
  action: "setDomains";
  // The IDs of the variable node whose domains are to be set
  nodeIds: string[];
  // The new domains of the nodes
  domains: string[][];
}

export interface ICSPHighlightNodesEvent extends IEvent {
  action: "highlightNodes";
  // The IDs of the nodes to highlight
  nodeIds: string[];
  // The colour of the highlight
  colour: string;
}

export interface ICSPChooseDomainSplitEvent extends IEvent {
  action: "chooseDomainSplit";
  // The domain to choose a split from
  domain: string[];
  var: string;
}

export interface ICSPChooseDomainSplitBeforeACEvent extends IEvent {
  action: "chooseDomainSplitBeforeAC";
}

export interface ICSPSetSolutionEvent extends IEvent {
  action: "setSolution";
  // The string representing the new solution
  solution: string;
}

export interface ICSPSetSplitEvent extends IEvent {
  action: "setSplit";
  // The string representing the domain of the splitted variable
  domain: string[];
  // The string representing the name of the splitted variable
  var: string;
}

export interface ICSPSetOrderEvent extends IEvent {
  action: "setOrder";
  // The string representing the name of the splitted variable
  var: string;
  // The string representing the first half domain of the splitted variable
  domain: string[];
  // The string representing the second half domain of the splitted variable
  other: string[];
}

export interface ICSPShowPositionsEvent extends IEvent {
  action: "showPositions";
  // The string representing the node positions
  positions: string;
}

// CSP Visualizer Events
export type Events =
  | ICSPHighlightArcsEvent
  | ICSPSetDomainsEvent
  | ICSPHighlightNodesEvent
  | ICSPChooseDomainSplitEvent
  | ICSPChooseDomainSplitBeforeACEvent
  | ICSPSetSolutionEvent
  | ICSPSetSplitEvent
  | ICSPSetOrderEvent
  | ICSPShowPositionsEvent
  | Events;
