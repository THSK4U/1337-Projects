/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_memmove.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: tsellak <tsellak@student.1337.ma>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/10/18 23:00:08 by tsellak           #+#    #+#             */
/*   Updated: 2025/11/03 14:28:32 by tsellak          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

void	*ft_memmove(void *dest, const void *src, size_t n)
{
	size_t			i;
	unsigned char	*v_dst;
	unsigned char	*v_src;

	if (!dest && !src)
		return (NULL);
	v_dst = (unsigned char *)dest;
	v_src = (unsigned char *)src;
	i = 0;
	if (v_dst > v_src)
	{
		while (n-- > 0)
			v_dst[n] = v_src[n];
	}
	else
	{
		while (i < n)
		{
			v_dst[i] = v_src[i];
			i++;
		}
	}
	return (dest);
}
