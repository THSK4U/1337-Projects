/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   push.c                                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: Tsellak <tsellak@student.1337.ma>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/12/25 22:00:16 by Tsellak           #+#    #+#             */
/*   Updated: 2026/01/07 10:42:55 by Tsellak          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "checker.h"

static void	push(t_stack **dest, t_stack **src)
{
	t_stack	*node_push;

	if (!src || !*src)
		return ;
	node_push = *src;
	*src = node_push->next;
	node_push->next = *dest;
	*dest = node_push;
}

void	pa(t_stack **a, t_stack **b)
{
	push(a, b);
}

void	pb(t_stack **b, t_stack **a)
{
	push(b, a);
}
